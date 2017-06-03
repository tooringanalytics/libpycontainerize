import re
import os


DEFAULT_PROJECTS_DIR = 'projects'

CONFIG_TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'config_templates',
)

CLASSES_DIR = 'classes'
TYPES_DIR = 'types'

OBJ_ATTR_TEMPLATES = '__templates__'
BASE_CLASS_NAME = '__base__'
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
PRJ_ATTR_SERVICES = 'services'
DOM_ATTR_APPS = 'apps'
DOM_ATTR_SERVICES = 'services'
LEAF_ATTR_CONF = 'conf'


INBUILT_TYPES = set([
    'str',
    'int',
    'float',
    'boolean',
    'list',
    'dict',
    '__type__',
    '__class__',
    '__template__'
])

RE_INBUILT_CONTAINERS = [
    re.compile(r'^list\((\w+)\)$'),
]

PROJECT_CONFIG_FILE = 'projectConfig.json'
DOMAIN_CONFIG_FILE = 'domainConfig.json'
APP_CONFIG_FILE = 'appConfig.json'

RE_LIST_OF_TYPES = re.compile(r'^list\((\w+)\)$')
