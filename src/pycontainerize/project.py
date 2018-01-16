import json
from json import JSONEncoder
import os

from errors import (
    UnableToLoadProject,
    UnableToLoadApp,
    UnableToRenderTemplate,
)
from constants import (
    CONTEXT_ATTRIB,
    PROJECT_ATTRIB,
    DOMAINS_ATTRIB,
    PARENT_ATTRIB,
    SERVICES_ATTRIB,
    NETWORKS_ATTRIB,
    DOMAINS_DIR,
    PROJECT_CONFIG,
    PROJECT_TEMPLATE_MAP,
)
from domain import (
    Domain,
)
from network import (
    Networks,
)


class ProjectEncoder(JSONEncoder):
    ''' Encode a Project object into a dict for JSON serialization '''
    def default(self, obj):
        ps = {}
        project = obj.project
        for key in project.keys():
            if key == DOMAINS_ATTRIB:
                ps[key] = [
                    domain.to_dict()
                    for domain in project[DOMAINS_ATTRIB]
                ]
            elif key == NETWORKS_ATTRIB:
                ps[key] = project[NETWORKS_ATTRIB].to_dict()
            else:
                ps[key] = project[key]
        return ps


class Project(object):
    ''' A Python App Container Swarm Project '''
    def __init__(self, project_dir, project_def):
        self.project = project_def
        self.dir = project_dir
        self.load_networks()
        self.load_domains()

    def load_networks(self):
        # load the network configuration
        if NETWORKS_ATTRIB in self.project and \
                self.project[NETWORKS_ATTRIB] is not None:
            self.project[NETWORKS_ATTRIB] = Networks.load(
                self.dir,
                self.project[NETWORKS_ATTRIB]
            )
        else:
            self.project[NETWORKS_ATTRIB] = Networks.load(
                self.dir,
                []
            )

    def load_domains(self):
        # load the domain configurations
        self.project[DOMAINS_ATTRIB] = [
            Domain.load(os.path.join(self.dir, DOMAINS_DIR, dom_name))
            for dom_name in self.project[DOMAINS_ATTRIB]
        ]

    @staticmethod
    def load(project_dir):
        project_file = os.path.join(project_dir, PROJECT_CONFIG)
        try:
            with open(project_file, "r") as prfp:
                project_def = json.load(prfp)
                return Project(project_dir, project_def)
        except UnableToLoadApp:
            raise
        except Exception as err:
            raise UnableToLoadProject(project_file + ': ' + str(err))

    def to_python(self):
        return self.to_dict()

    def to_dict(self):
        return ProjectEncoder().default(self)

    def __str__(self):
        return json.dumps(
            self,
            cls=ProjectEncoder,
            ensure_ascii=True,
            indent=4,
            sort_keys=True,
            separators=(',', ': '),
        )

    def render(self,
               renderer,
               output_dir):
        ''' Render the templates for this project '''
        # Set up the rendering context
        serialized_project = self.to_dict()
        context = {
            CONTEXT_ATTRIB: PROJECT_ATTRIB,
            PARENT_ATTRIB: serialized_project,
            PROJECT_ATTRIB: serialized_project
        }
        # Render each template file in PROJECT_TEMPLATE_MAP
        for (src, dst) in PROJECT_TEMPLATE_MAP.items():
            try:
                # Interpolate all variables in the destination
                # path
                dst = renderer.render_template_from_string(
                    dst,
                    context
                )
                output_path = os.path.join(output_dir, dst)
                output_parent = os.path.dirname(output_path)
                # Create the path if it does not exist
                if not os.path.exists(output_parent):
                    os.makedirs(output_parent)
                # Render the template under the project's context
                renderer.render_template(src,
                                         context,
                                         output_path)
            except Exception as err:
                raise UnableToRenderTemplate(src + ': ' + str(err))
        # Render the templates for all services within this project
        for service in self.project[SERVICES_ATTRIB]:
            service.render(context, renderer, output_dir)
        # Render the templates for all Domains within this project
        for domain in self.project[DOMAINS_ATTRIB]:
            domain.render(serialized_project, renderer, output_dir)
