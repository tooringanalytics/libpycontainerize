import os
import re

DEFAULT_OUTPUT_DIR = 'output'


DEFAULT_PROJECTS_DIR = os.path.join(
    DEFAULT_OUTPUT_DIR,
    'projects'
)

CONFIG_TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'config_templates',
)

CLASSES_DIR = 'classes'
TYPES_DIR = 'types'

OBJ_ATTR_NAME = 'name'
OBJ_ATTR_PARENTS = '__parents__'
OBJ_ATTR_TEMPLATES = '__templates__'
OBJ_ATTR_CONFIG_TEMPLATE = '__config_template__'
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
ATTR_CTX = 'ctx'
ATTR_DST = 'dst'

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
SERVICE_CONFIG_FILE = 'serviceConfig.json'

RE_LIST_OF_TYPES = re.compile(r'^list\((\w+)\)$')

PROJECT_SERVICE_TEMPLATE_PATH_PREFIX = 'services/{{ service.name }}'
DOMAIN_SERVICE_TEMPLATE_PATH_PREFIX = 'domains/{{ domain.name }}/services/{{ service.name }}'
APP_TEMPLATE_PATH_PREFIX = 'domains/{{ domain.service }}/apps/{{ app.name }}'

DEFAULT_PERMS = '660'
