DEFAULT_PROJECTS_DIR = 'projects'
DEFAULT_OUTPUT_DIR = 'output'
DEFAULT_TEMPLATES_DIR = 'templates'

APP_CONFIG = 'appConfig.json'
SERVICE_CONFIG = 'serviceConfig.json'
PROJECT_CONFIG = 'projectConfig.json'
NETWORKS_CONFIG = 'networksConfig.json'
DOMAIN_CONFIG = 'domainConfig.json'

APPS_DIR = 'apps'
SERVICES_DIR = 'services'
DOMAINS_DIR = 'domains'
CERTS_DIR = 'certs'

# Object attributes
CONTEXT_ATTRIB = 'context'
APPS_ATTRIB = 'apps'
SERVICES_ATTRIB = 'services'
NETWORKS_ATTRIB = 'networks'
DOMAINS_ATTRIB = 'domains'
NGINX_ATTRIB = 'nginx'
NAME_ATTRIB = 'name'

# Context attributes
APP_ATTRIB = 'app'
SERVICE_ATTRIB = 'service'
PROJECT_ATTRIB = 'project'
DOMAIN_ATTRIB = 'domain'

# Templates to be rendered in Project Context
PROJECT_TEMPLATE_MAP = {
    'docker/docker-compose.yml.template': 'docker-compose.yml',
    'docker/only-services.yml.template': 'only-services.yml',
    'services/nginx/nginx.conf': 'services/nginx/nginx.conf',
    'services/nginx/supervisor-app.conf': 'services/nginx/supervisor-app.conf',
    'services/mongodb/entrypoint.sh': 'services/mongodb/entrypoint.sh',

}

# Templates to be rendered in Domain Context
DOMAIN_TEMPLATE_MAP = {
    'domain/nginx-app.conf': 'services/nginx/sites-enabled/{{ domain.name }}.conf',
}

# Templates to be rendered in Service Context
SERVICE_TEMPLATE_MAP = {
    'domainService/server.env': 'domains/{{ domain.name }}/services/{{ service.name }}/server.env',
    'domainService/supervisor-app.conf': 'domains/{{ domain.name }}/services/{{ service.name }}/supervisor-app.conf',
    'domainService/supervisord.conf': 'domains/{{ domain.name }}/services/{{ service.name }}/supervisord.conf',
    'domainService/configure-app.sh': 'domains/{{ domain.name }}/services/{{ service.name }}/configure-app.sh',
    'domainService/exec_cmd_wrapper.sh': 'domains/{{ domain.name }}/services/{{ service.name }}/exec_cmd_wrapper.sh',
}

# Templates to be rendered in App Context
APP_TEMPLATE_MAP = {
    'djangoapp/server.env': 'domains/{{ domain.name }}/apps/{{ app.name }}/server.env',
    'djangoapp/supervisor-app.conf': 'domains/{{ domain.name }}/apps/{{ app.name }}/supervisor-app.conf',
    'djangoapp/uwsgi.ini': 'domains/{{ domain.name }}/apps/{{ app.name }}/uwsgi.ini',
    'djangoapp/uwsgi_params': 'services/nginx/uwsgi/{{ domain.name }}/{{ app.name }}/uwsgi_params',
    'djangoapp/configure-app.sh': 'domains/{{ domain.name }}/apps/{{ app.name }}/configure-app.sh',
    'djangoapp/create_user.sql': 'services/{{ project.services.postgres.alias }}/initdb/{{ app.name }}_01_create_user.sql',
    'djangoapp/create_database.sql': 'services/{{ project.services.postgres.alias }}/initdb/{{ app.name }}_02_create_database.sql',
}
