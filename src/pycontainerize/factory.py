import sys
import os
import json
import argparse
import six
import re
from errors import (
    InvalidTypeError,
    TypeDefinitionError,
)
from project import (
    Project,
)
DEFAULT_PROJECTS_DIR = 'projects'

CONFIG_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__),
    'config_templates',
)

CLASSES_DIR = 'classes'
TYPES_DIR = 'types'

BASE_CLASS_NAME = 'base'
ATTR_EXTENDS = 'extends'
ATTR_DEFINITION = 'definition'
ATTR_TEMPLATES = 'templates'
ATTR_NAME = 'name'
ATTR_REQUIRED = 'required'
ATTR_TYPE = 'type'
ATTR_DEFAULT = 'default'
ATTR_SRC = 'src'
ATTR_PERM = 'perm'

PRJ_ATTR_DOMAINS = 'domains'

INBUILT_TYPES = set([
    'str',
    'int',
    'float',
    'boolean',
    'list',
    'dict',
])

PROJECT_CONFIG_FILE = 'projectConfig.json'
DOMAIN_CONFIG_FILE = 'domainConfig.json'
APP_CONFIG_FILE = 'appConfig.json'

RE_LIST_OF_TYPES = re.compile(r'^list\((\w+)\)$')


class ObjectProto(object):
    '''A Skeleton Object Prototype used to hold attributes'''
    pass


class ObjectConfig(object):
    '''Base class for all containerizer object configurations'''
    def __init__(self):
        self.obj = ObjectProto()

    def initialize(self, obj=None):
        '''Load and parse the configuration template for this object'''
        config_template = self.load_config_template()
        self.parse_config_template(config_template, obj)
        self.config_template = config_template

    def load_config_template(self):
        '''Load the configuration template for this object'''
        config_template_path = os.path.join(
            CONFIG_TEMPLATES_DIR,
            self.config_template_file
        )
        try:
            with open(config_template_path, 'r') as fp:
                config_template = json.load(fp)
        except IOError as e:
            raise InvalidTypeError(str(e))
        except ValueError as e:
            raise TypeDefinitionError(config_template_path + ': ' + str(e))
        return config_template

    def parse_config_template(self, config_template, obj=None):
        if obj is not None:
            self.obj = obj
        '''Parse the given configuration template'''
        for attrib in config_template:
            if attrib[ATTR_REQUIRED]:
                if attrib[ATTR_TYPE] in INBUILT_TYPES:
                    setattr(self.obj, attrib[ATTR_NAME], attrib[ATTR_DEFAULT])
                else:
                    type_name = attrib[ATTR_TYPE]
                    type_config = TypeConfig(type_name)
                    type_config.initialize()
                    setattr(self.obj, attrib[ATTR_NAME], type_config)

    def to_python(self):
        '''Traverse the object tree and generate a python representation'''
        json_rep = {}
        for attrib in self.config_template:
            if hasattr(self.obj, attrib[ATTR_NAME]):
                if attrib[ATTR_TYPE] in INBUILT_TYPES:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                elif RE_LIST_OF_TYPES.match(attrib[ATTR_TYPE]):
                    lst = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                    json_rep[attrib[ATTR_NAME]] = [
                        obj.to_python()
                        for obj in lst
                    ]
                else:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj, attrib[ATTR_NAME]
                    ).to_python()
        return json_rep


class ClassConfig(ObjectConfig):
    '''Configuration object for service and application classes'''
    def __init__(self, class_name):
        self.config_template_dir = os.path.join(
            CLASSES_DIR,
            class_name,
        )
        self.config_template_file = os.path.join(
            self.config_template_dir,
            '.'.join((class_name, 'json'))
        )
        super(ClassConfig, self).__init__()

    def copy_templates(self, templates):
        for template in templates:
            template_file = template[ATTR_SRC]
            template_perm = template[ATTR_PERM]

    def parse_config_template(self, config_template):
        if ATTR_NAME in config_template:
            setattr(self.obj, ATTR_NAME, config_template[ATTR_NAME])
        if ATTR_EXTENDS in config_template:
            base_classes = config_template[ATTR_EXTENDS]
        if ATTR_DEFINITION in config_template:
            type_definitions = config_template[ATTR_DEFINITION]
        if ATTR_TEMPLATES in config_template:
            templates = config_template[ATTR_DEFINITION]
        base_class_config = ClassConfig(BASE_CLASS_NAME)
        base_class_config.initialize(self.obj)
        for base_class in base_classes:
            base_class_config = ClassConfig(base_class)
            base_class_config.initialize(self.obj)
        self.copy_templates(templates)
        super(ClassConfig, self).parse_config_template(type_definitions)

    def to_python(self):
        '''Traverse the object tree and generate a python representation'''
        json_rep = {}
        for attrib in self.config_template[ATTR_DEFINITION]:
            if hasattr(self.obj, attrib[ATTR_NAME]):
                if attrib[ATTR_TYPE] in INBUILT_TYPES:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                elif RE_LIST_OF_TYPES.match(attrib[ATTR_TYPE]):
                    lst = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                    json_rep[attrib[ATTR_NAME]] = [
                        obj.to_python()
                        for obj in lst
                    ]
                else:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj, attrib[ATTR_NAME]
                    ).to_python()
        return json_rep


class TypeConfig(ObjectConfig):
    '''Configuration object for cutom types'''
    def __init__(self, type_name):
        self.config_template_file = os.path.join(
            TYPES_DIR,
            '.'.join((type_name, 'json'))
        )
        super(TypeConfig, self).__init__()


class ProjectConfig(ObjectConfig):
    '''Configuration object for projects'''
    config_template_file = 'projectConfigTemplate.json'


class DomainConfig(ObjectConfig):
    '''Configuration object for domains'''
    config_template_file = 'domainConfigTemplate.json'


class AppConfig(ObjectConfig):
    '''Configuration object for apps'''
    config_template_file = 'appConfigTemplate.json'


class ServiceConfig(ObjectConfig):
    '''Configuration object for services'''
    config_template_file = 'serviceConfigTemplate.json'


class ObjectFactory(object):
    '''Factory class for creating various types of configuration files'''

    def create_project(self, project_config):
        '''Creates a project from the given configuration template'''
        return project_config.to_python()

    def create_domain(self, project, domain_config):
        project[PRJ_ATTR_DOMAINS].append(domain_config.obj.name)
        return domain_config.to_python()

    def remove_domain(self, project, domain_name):
        pass

    def create_app(self, domain, app_config):
        return app_config.to_python()

    def remove_app(self, domain, app_name):
        pass

    def create_project_service(self, project, service_config):
        return service_config.to_python()

    def remove_project_service(self, project, service_name):
        pass

    def create_domain_service(self, domain, service_config):
        return service_config.to_python()

    def remove_domain_service(self, domain, service_name):
        pass


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
            args.domain_name
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

        create_domain_parser = subparsers.add_parser(
            'create_domain',
            help='Create a new domain inside a project'
        )

        # Setup options for parser
        self.init_create_domain_parser(create_domain_parser)

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
