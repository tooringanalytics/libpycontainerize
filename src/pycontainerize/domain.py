import json
from json import JSONEncoder
import os

from service import (
    Service,
)
from app import (
    App,
)
from utils import (
    dircopy,
)
from constants import (
    DOMAINS_DIR,
    DOMAIN_TEMPLATE_MAP,
    DOMAIN_CONFIG,
    DOMAIN_ATTRIB,
    CONTEXT_ATTRIB,
    PROJECT_ATTRIB,
    APPS_ATTRIB,
    APPS_DIR,
    SERVICES_ATTRIB,
    SERVICES_DIR,
    CERTS_DIR,
    NAME_ATTRIB,
)
from errors import (
    UnableToLoadDomain,
    UnableToRenderTemplate,
)


class DomainEncoder(JSONEncoder):
    ''' Encode a Domain object into a dict for JSON serialization '''
    def default(self, obj):
        ps = {}
        domain = obj.domain
        for key in domain.keys():
            if key == APPS_ATTRIB:
                ps[key] = [
                    app.to_dict()
                    for app in domain[APPS_ATTRIB]
                ]
            elif key == SERVICES_ATTRIB:
                ps[key] = [
                    service.to_dict()
                    for service in domain[SERVICES_ATTRIB]
                ]
            else:
                ps[key] = domain[key]
        return ps


class Domain(object):
    ''' A domain that hosts various apps under its directories '''
    def __init__(self, domain_dir, domain_def):
        self.domain = domain_def
        self.dir = domain_dir
        self.load_services()
        self.load_apps()

    def load_services(self):
        """ load the service configurations """
        self.domain['services'] = [
            Service.load(os.path.join(self.dir, SERVICES_DIR, service_name))
            for service_name in self.domain[SERVICES_ATTRIB]
        ]

    def load_apps(self):
        """ load the app configurations """
        self.domain['apps'] = [
            App.load(os.path.join(self.dir, APPS_DIR, app_name))
            for app_name in self.domain[APPS_ATTRIB]
        ]

    @staticmethod
    def load(domain_dir):
        """ Load the domain configuration """
        domain_file = os.path.join(domain_dir, DOMAIN_CONFIG)
        try:
            with open(domain_file, "r") as domfp:
                domain = json.load(domfp)
                return Domain(domain_dir, domain)
        except Exception as err:
            raise UnableToLoadDomain(domain_file + ': ' + str(err))

    def __str__(self):
        return json.dumps(
            self,
            cls=DomainEncoder,
            ensure_ascii=True,
            indent=4,
            separators=(': ', ','),
        )

    def render(self,
               project,
               renderer,
               output_dir):
        context = {}
        context[CONTEXT_ATTRIB] = DOMAIN_ATTRIB
        context[DOMAIN_ATTRIB] = self.to_dict()
        context[PROJECT_ATTRIB] = project

        for (src, dst) in DOMAIN_TEMPLATE_MAP.items():
            try:
                dst = renderer.render_template_from_string(
                    dst,
                    context
                )
                output_path = os.path.join(output_dir, dst)
                output_parent = os.path.dirname(output_path)
                if not os.path.exists(output_parent):
                    os.makedirs(output_parent)
                # import pdb; pdb.set_trace()
                renderer.render_template(src,
                                         context,
                                         output_path)
            except Exception as err:
                raise UnableToRenderTemplate(src + ': ' + str(err))
            # Render the templates for all Services within this domain
            for service in self.domain[SERVICES_ATTRIB]:
                service.render(project, self.to_dict(), renderer, output_dir)
            # Render the templates for all Apps within this domain
            for app in self.domain[APPS_ATTRIB]:
                app.render(project, self.to_dict(), renderer, output_dir)
            # Copy Certificates and keys
            certs_dir = os.path.join(self.dir,
                                     CERTS_DIR)
            output_certs_dir = os.path.join(output_dir,
                                            DOMAINS_DIR,
                                            self.domain[NAME_ATTRIB],
                                            CERTS_DIR)
        dircopy(certs_dir, output_certs_dir)

    def to_python(self):
        return self.to_dict()

    def to_dict(self):
        return DomainEncoder().default(self)
