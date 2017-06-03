import sys
import os
import json
import argparse
import six
from pycontainerize.project import (
    Project,
)
from pycontainerize.domain import (
    Domain,
)
from project_config import (
    ProjectConfig,
)
from domain_config import (
    DomainConfig,
)
from app_config import (
    AppConfig,
)
from service_config import (
    ServiceConfig,
)
from object_factory import (
    ObjectFactory,
)
from constants import (
    DOM_ATTR_APPS,
    APP_CONFIG_FILE,
    DOMAIN_CONFIG_FILE,
    PRJ_ATTR_DOMAINS,
    DEFAULT_PROJECTS_DIR,
    PROJECT_CONFIG_FILE,
)


class FactoryApp(object):
    ''' Main application class '''

    def __init__(self):
        self.parser = self.init_argparse()

    def exec_create_project(self, args, extra_args):
        project_config = ProjectConfig()
        project_config.initialize()
        project_config.obj.name = args.project_name

        if args.version:
            project_config.obj.version = args.version

        factory = ObjectFactory()

        project = factory.create_project(project_config)

        projects_dir = DEFAULT_PROJECTS_DIR \
            if args.projects_dir is None else args.projects_dir

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

    def exec_create_domain(self, args, extra_args):
        projects_dir = DEFAULT_PROJECTS_DIR \
            if args.projects_dir is None else args.projects_dir

        project_root = os.path.join(
            projects_dir,
            args.project_name
        )

        project = Project.load(project_root).to_python()

        domain_config = DomainConfig()
        domain_config.initialize()
        domain_config.obj.name = args.domain_name

        factory = ObjectFactory()

        domain = factory.create_domain(project, domain_config)

        domain_root = os.path.join(
            project_root,
            PRJ_ATTR_DOMAINS,
            args.domain_name,
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

    def exec_create_app(self, args, extra_args):
        projects_dir = DEFAULT_PROJECTS_DIR \
            if args.projects_dir is None else args.projects_dir

        project_root = os.path.join(
            projects_dir,
            args.project_name
        )

        project = Project.load(project_root).to_python()

        domain_root = os.path.join(
            project_root,
            PRJ_ATTR_DOMAINS,
            args.domain_name,
        )

        domain = Domain.load(domain_root)

        app_config = AppConfig()
        app_config.initialize()
        app_config.obj.name = args.app_name

        factory = ObjectFactory()

        app = factory.create_app(domain, app_config)

        app_root = os.path.join(
            domain_root,
            DOM_ATTR_APPS,
            args.app_name,
        )

        if not os.path.exists(app_root):
            os.makedirs(app_root)

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

    def execute(self, parser, args):
        extra_args = self.parse_extra(parser, args)
        if args.subparser_name == 'create_project':
            self.exec_create_project(args, extra_args)
        elif args.subparser_name == 'create_domain':
            self.exec_create_domain(args, extra_args)

    def parse_extra(self, parser, namespace):
        '''This function takes the 'extra' attribute from global
        namespace and re-parses it to create separate namespaces
        for all other chained commands.
        '''
        namespaces = []
        extra = namespace.extra
        while extra:
            n = parser.parse_args(extra)
            extra = n.extra
            namespaces.append(n)
        return namespaces

    def init_argparse(self):
        argparser = argparse.ArgumentParser()

        subparsers = argparser.add_subparsers(
            help='sub-command help',
            dest='subparser_name'
        )

        # Add nargs="*" for zero or more other commands
        argparser.add_argument(
            'extra',
            nargs='*',
            help='Other commands'
        )

        create_project_parser = subparsers.add_parser(
            'create_project',
            help='Create a new project'
        )

        # Setup options for parser
        self.init_create_project_parser(create_project_parser)

        create_project_service_parser = subparsers.add_parser(
            'create_project_service',
            help='Create a new service for the given project'
        )

        # Setup options for parser
        self.init_create_project_service_parser(create_project_service_parser)

        create_domain_parser = subparsers.add_parser(
            'create_domain',
            help='Create a new domain inside a project'
        )

        # Setup options for parser
        self.init_create_domain_parser(create_domain_parser)

        create_domain_service_parser = subparsers.add_parser(
            'create_domain_service',
            help='Create a new service inside a domain'
        )

        # Setup options for parser
        self.init_create_domain_service_parser(create_domain_service_parser)

        return argparser

    def init_create_project_parser(self, parser):
        '''Setup options for create_project'''
        parser.add_argument(
            'project_name',
            help='Name of the project'
        )

        parser.add_argument(
            '-v',
            '--version',
            help='project version',
        )

        parser.add_argument(
            '-p',
            '--projects-dir',
            help='Output directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        return parser

    def init_create_project_service_parser(self, parser):
        '''Setup options for create_project_service'''
        parser.add_argument(
            'project_name',
            help='Name of the project'
        )

        parser.add_argument(
            'service_name',
            help='Name of the service'
        )

        parser.add_argument(
            '-p',
            '--projects-dir',
            help='Output directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        return parser

    def init_create_domain_parser(self, parser):
        '''Setup options for create_domain'''
        parser.add_argument(
            'project_name',
            help='Name of the project'
        )

        parser.add_argument(
            'domain_name',
            help='Name of the domain'
        )

        parser.add_argument(
            '-p',
            '--projects-dir',
            help='Output directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        return parser

    def init_create_domain_service_parser(self, parser):
        '''Setup options for create_domain_service'''
        parser.add_argument(
            'project_name',
            help='Name of the project'
        )

        parser.add_argument(
            'domain_name',
            help='Name of the domain'
        )

        parser.add_argument(
            'service_name',
            help='Name of the service'
        )

        parser.add_argument(
            '-p',
            '--projects-dir',
            help='Output directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        return parser

    def init_create_app_parser(self, parser):
        '''Setup options for create_app'''
        parser.add_argument(
            'project_name',
            help='Name of the project'
        )

        parser.add_argument(
            'domain_name',
            help='Name of the domain'
        )

        parser.add_argument(
            'app_name',
            help='Name of the app'
        )

        parser.add_argument(
            '-p',
            '--projects-dir',
            help='Output directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        return parser

    def main(self):
        args = self.parser.parse_args()
        try:
            self.execute(self.parser, args)
        except Exception as err:
            print(err)
            six.reraise(type(err), err, sys.exc_info()[2])


if __name__ == '__main__':
    app = FactoryApp()
    app.main()
