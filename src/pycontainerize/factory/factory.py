import json
import os

import click
from pycontainerize.factory.app_config import AppConfig
from pycontainerize.factory.constants import APP_CONFIG_FILE
from pycontainerize.factory.constants import DEFAULT_PROJECTS_DIR
from pycontainerize.factory.constants import DOM_ATTR_APPS
from pycontainerize.factory.constants import DOM_ATTR_SERVICES
from pycontainerize.factory.constants import DOMAIN_CONFIG_FILE
from pycontainerize.factory.constants import PRJ_ATTR_DOMAINS
from pycontainerize.factory.constants import PRJ_ATTR_SERVICES
from pycontainerize.factory.constants import PROJECT_CONFIG_FILE
from pycontainerize.factory.constants import SERVICE_CONFIG_FILE
from pycontainerize.factory.domain_config import DomainConfig
from pycontainerize.factory.object_factory import ObjectFactory
from pycontainerize.factory.project_config import ProjectConfig
from pycontainerize.factory.service_config import ServiceConfig

from pycontainerize.domain import Domain
from pycontainerize.project import Project


@click.command()
@click.option('-v', '--version', help='Project version')
@click.option('-p', '--projects-dir', help='Project directory')
@click.argument('project_name')
def create_project(project_name,
                   version='',
                   projects_dir=DEFAULT_PROJECTS_DIR):
    project_config = ProjectConfig()
    project_config.initialize()
    project_config.obj.name = project_name

    if version:
        project_config.obj.version = version

    factory = ObjectFactory()

    project = factory.create_project(project_config)

    projects_dir = DEFAULT_PROJECTS_DIR \
        if projects_dir is None else projects_dir

    project_root = os.path.join(
        projects_dir,
        project_config.obj.name
    )

    if not os.path.exists(project_root):
        os.makedirs(project_root)

    output_file = os.path.join(
        project_root,
        PROJECT_CONFIG_FILE,
    )

    with open(output_file, 'w') as fp:
        json.dump(
            project,
            fp,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )


@click.command()
@click.option('-p', '--projects-dir', help='Project directory')
@click.argument('project_name')
@click.argument('domain_name')
def create_domain(project_name,
                  domain_name,
                  projects_dir=DEFAULT_PROJECTS_DIR):
    projects_dir = DEFAULT_PROJECTS_DIR \
        if projects_dir is None else projects_dir

    project_root = os.path.join(
        projects_dir,
        project_name
    )

    project = Project.load(project_root).to_python()

    domain_config = DomainConfig()
    domain_config.initialize()
    domain_config.obj.name = domain_name

    factory = ObjectFactory()

    domain = factory.create_domain(project, domain_config)

    domain_root = os.path.join(
        project_root,
        PRJ_ATTR_DOMAINS,
        domain_name,
    )

    if not os.path.exists(domain_root):
        os.makedirs(domain_root)

    output_file = os.path.join(
        domain_root,
        DOMAIN_CONFIG_FILE,
    )

    with open(output_file, 'w') as fp:
        json.dump(
            domain,
            fp,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )

    if not os.path.exists(project_root):
        os.makedirs(project_root)

    output_file = os.path.join(
        project_root,
        PROJECT_CONFIG_FILE,
    )

    with open(output_file, 'w') as fp:
        json.dump(
            project,
            fp,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )


@click.command()
@click.option('-p', '--projects-dir', help='Project directory')
@click.option('-e', '--extends', help='Class')
@click.option('-d', '--definitions', help='Custom Type Definitions File')
@click.option('-t', '--templates', help='Custom Template Defintions File')
@click.argument('project_name')
@click.argument('domain_name')
@click.argument('app_name')
def create_app(project_name,
               domain_name,
               app_name,
               projects_dir=DEFAULT_PROJECTS_DIR,
               extends=[],
               definitions=None,
               templates=None):
        projects_dir = DEFAULT_PROJECTS_DIR \
            if projects_dir is None else projects_dir

        project_root = os.path.join(
            projects_dir,
            project_name
        )

        # project = Project.load(project_root).to_python()

        domain_root = os.path.join(
            project_root,
            PRJ_ATTR_DOMAINS,
            domain_name,
        )

        domain = Domain.load(domain_root).to_python()

        extends = extends.split(',')
        if definitions is not None:
            with open(definitions, 'r') as fp:
                definitions = json.load(fp)
        else:
            definitions = []
        if templates is not None:
            with open(templates, 'r') as fp:
                templates = json.load(fp)
        else:
            templates = []

        app_config = AppConfig(
            name=app_name,
            extends=extends,
            definitions=definitions,
            templates=templates,
        )
        app_config.initialize()
        app_config.obj.name = app_name

        factory = ObjectFactory()

        app = factory.create_app(domain, app_config)

        app_root = os.path.join(
            domain_root,
            DOM_ATTR_APPS,
            app_name,
        )

        if not os.path.exists(app_root):
            os.makedirs(app_root)

        app_config.copy_templates(app_root)

        output_file = os.path.join(
            app_root,
            APP_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                app,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

        if not os.path.exists(domain_root):
            os.makedirs(domain_root)

        output_file = os.path.join(
            domain_root,
            DOMAIN_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                domain,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )


@click.command()
@click.option('-p', '--projects-dir', help='Project directory')
@click.option('-e', '--extends', help='Class')
@click.option('-d', '--definitions', help='Custom Type Definitions File')
@click.option('-t', '--templates', help='Custom Template Defintions File')
@click.argument('project_name')
@click.argument('domain_name')
@click.argument('service_name')
def create_domain_service(project_name,
                          domain_name,
                          service_name,
                          projects_dir=DEFAULT_PROJECTS_DIR,
                          extends=[],
                          definitions=None,
                          templates=None):
        projects_dir = DEFAULT_PROJECTS_DIR \
            if projects_dir is None else projects_dir

        project_root = os.path.join(
            projects_dir,
            project_name
        )

        # project = Project.load(project_root).to_python()

        domain_root = os.path.join(
            project_root,
            PRJ_ATTR_DOMAINS,
            domain_name,
        )

        domain = Domain.load(domain_root).to_python()

        extends = extends.split(',')
        if definitions is not None:
            with open(definitions, 'r') as fp:
                definitions = json.load(fp)
        else:
            definitions = []
        if templates is not None:
            with open(templates, 'r') as fp:
                templates = json.load(fp)
        else:
            templates = []

        service_config = ServiceConfig(
            name=service_name,
            extends=extends,
            definitions=definitions,
            templates=templates,
        )
        service_config.initialize()
        service_config.obj.name = service_name

        factory = ObjectFactory()

        service = factory.create_domain_service(domain, service_config)

        service_root = os.path.join(
            domain_root,
            DOM_ATTR_SERVICES,
            service_name,
        )

        if not os.path.exists(service_root):
            os.makedirs(service_root)

        service_config.copy_templates(service_root)

        output_file = os.path.join(
            service_root,
            SERVICE_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                service,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

        if not os.path.exists(domain_root):
            os.makedirs(domain_root)

        output_file = os.path.join(
            domain_root,
            DOMAIN_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                domain,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )


@click.command()
@click.option('-p', '--projects-dir', help='Project directory')
@click.option('-e', '--extends', help='Class')
@click.option('-d', '--definitions', help='Custom Type Definitions File')
@click.option('-t', '--templates', help='Custom Template Defintions File')
@click.argument('project_name')
@click.argument('service_name')
def create_project_service(project_name,
                           service_name,
                           projects_dir=DEFAULT_PROJECTS_DIR,
                           extends=[],
                           definitions=None,
                           templates=None):
        projects_dir = DEFAULT_PROJECTS_DIR \
            if projects_dir is None else projects_dir

        project_root = os.path.join(
            projects_dir,
            project_name
        )

        project = Project.load(project_root).to_python()

        service_root = os.path.join(
            project_root,
            PRJ_ATTR_SERVICES,
            service_name,
        )

        extends = extends.split(',')

        if definitions is not None:
            with open(definitions, 'r') as fp:
                definitions = json.load(fp)
        else:
            definitions = []

        if templates is not None:
            with open(templates, 'r') as fp:
                templates = json.load(fp)
        else:
            templates = []

        service_config = ServiceConfig(
            name=service_name,
            extends=extends,
            definitions=definitions,
            templates=templates,
        )
        service_config.initialize()
        service_config.obj.name = service_name

        factory = ObjectFactory()

        service = factory.create_project_service(project, service_config)

        if not os.path.exists(service_root):
            os.makedirs(service_root)

        service_config.copy_templates(service_root)

        output_file = os.path.join(
            service_root,
            SERVICE_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                service,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

        if not os.path.exists(project_root):
            os.makedirs(project_root)

        output_file = os.path.join(
            project_root,
            PROJECT_CONFIG_FILE,
        )

        with open(output_file, 'w') as fp:
            json.dump(
                project,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )


@click.group()
def gen():
    pass


if __name__ == '__main__':
    gen.add_command(create_project)
    gen.add_command(create_domain)
    gen.add_command(create_app)
