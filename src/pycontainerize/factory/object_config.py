import json
import os

from constants import ATTR_DEFAULT
from constants import ATTR_NAME
from constants import ATTR_REQUIRED
from constants import ATTR_TYPE
from constants import CONFIG_TEMPLATES_DIR
from constants import INBUILT_TYPES
from constants import RE_INBUILT_CONTAINERS
from constants import RE_LIST_OF_TYPES
from constants import TYPES_DIR

from pycontainerize.errors import InvalidTypeError
from pycontainerize.errors import TypeDefinitionError
from pycontainerize.errors import TypeDefinitionNotFoundError


class ObjectProto(object):
    '''A Skeleton Object Prototype used to hold attributes'''

    def __init__(self):
        self.__templates__ = []


class ObjectConfig(object):
    '''Base class for all containerizer object configurations'''

    def __init__(self, typedef_search_paths=[]):
        if not typedef_search_paths:
            typedef_search_paths = [
                os.path.join(CONFIG_TEMPLATES_DIR, TYPES_DIR),
                CONFIG_TEMPLATES_DIR,
            ]
        self.obj = ObjectProto()
        self.typedef_search_paths = typedef_search_paths

    def initialize(self, obj=None):
        '''Load and parse the configuration template for this object'''
        config_template = self.load_config_template()
        self.parse_config_template(config_template, obj)
        self.config_template = config_template

    def load_config_template(self):
        '''Load the configuration template for this object'''
        config_template_path = None
        for search_path in self.typedef_search_paths:
            config_template_path = os.path.join(
                search_path,
                self.config_template_file
            )
            if os.path.exists(config_template_path):
                break
        if config_template_path is None or \
                not os.path.exists(config_template_path):
            config_template_path = os.path.join(
                CONFIG_TEMPLATES_DIR,
                self.config_template_file
            )
        if not os.path.exists(config_template_path):
            raise TypeDefinitionNotFoundError(
                'Cannot find definition file {}. Tried Paths: {}'.format(
                    self.config_template_file,
                    self.typedef_search_paths + [CONFIG_TEMPLATES_DIR],
                ))
        try:
            with open(config_template_path, 'r') as fp:
                config_template = json.load(fp)
        except IOError as e:
            raise InvalidTypeError(str(e))
        except ValueError as e:
            raise TypeDefinitionError(config_template_path + ': ' + str(e))
        self.config_template_path = config_template_path
        return config_template

    def is_inbuilt_container(self, attr_type):
        for reg in RE_INBUILT_CONTAINERS:
            if reg.match(attr_type):
                return True
        return False

    def parse_attributes(self, config_template):
        '''Parse the given configuration template'''
        for attrib in config_template:
            if attrib[ATTR_REQUIRED]:
                if attrib[ATTR_TYPE] in INBUILT_TYPES or \
                        self.is_inbuilt_container(attrib[ATTR_TYPE]):
                    setattr(
                        self.obj,
                        attrib[ATTR_NAME],
                        attrib[ATTR_DEFAULT]
                    )
                else:
                    type_name = attrib[ATTR_TYPE]
                    typedef_search_paths = self.get_typedef_search_paths()
                    type_config = TypeConfig(type_name, typedef_search_paths)
                    type_config.initialize()
                    setattr(self.obj, attrib[ATTR_NAME], type_config)

    def parse_config_template(self, config_template, obj=None):
        if obj is not None:
            self.obj = obj
        self.parse_attributes(config_template)

    def get_typedef_search_paths(self):
        return [
            os.path.join(CONFIG_TEMPLATES_DIR, TYPES_DIR),
            os.path.join(
                os.path.dirname(self.config_template_path),
                TYPES_DIR
            ),
            os.path.dirname(self.config_template_path)
        ]

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


class TypeConfig(ObjectConfig):
    '''Configuration object for cutom types'''

    def __init__(self, type_name, typedef_search_paths=[]):
        self.config_template_file = '.'.join((type_name, 'json'))
        super(TypeConfig, self).__init__(
            typedef_search_paths=typedef_search_paths
        )
