#!/usr/bin/env python
import os
import os.path

from fabric.api import env
from fabric.api import runs_once
from fabric.api import task
from fabric.context_managers import cd
from fabric.operations import put
from fabric.operations import run
from fabric.operations import settings

import pycontainerize
from pycontainerize import Containerizer

LOCAL_KEYFILE = os.path.join(
    os.environ['HOME'],
    'tooringanalytics_aws_ec2_debian_instance.pem'
)


def load_project(project_name):
    containerizer = Containerizer()
    project = containerizer.load_project(project_name)
    return project


def get_domain(project, domain_name):
    for domain in project['domains']:
        if domain['name'] == domain_name:
            return domain
    return None


def get_app(project, domain_name, app_name):
    domain = get_domain(project, domain_name)
    if domain:
        for app in domain['apps']:
            if app['name'] == app_name:
                return app
    return None


def get_service(project, domain_name, service_name):
    domain = get_domain(project, domain_name)
    if domain:
        for service in domain['services']:
            if service['name'] == service_name:
                return service
    return None


@task
def using_project(project_name):

    env.project_name = project_name

    project = load_project(project_name)

    project = project.to_dict()

    env.local_project_dir = os.path.join(
        pycontainerize.DEFAULT_OUTPUT_DIR,
        project['name'],
    )
    env.local_home = os.environ['HOME']
    # env.hosts = ['169.45.108.55']  # Koding VM for hackathon
    # env.hosts = ['50.116.12.111']  # Linode VM
    env.hosts = project['deploy']['hosts']  # Localhost
    env.user = project['deploy']['user']

    # key_filename
    # May be a string or list of strings, referencing file paths to SSH key
    # files to try when connecting. Passed through directly to the
    # SSH layer.
    # May be set/appended to with -i.
    env.key_filename = LOCAL_KEYFILE

    env.server_root_dir = '/home/' + env.user
    env.server_project_dir = os.path.join(
        env.server_root_dir,
        project['name']
    )
    env.server_domains_dir = os.path.join(
        env.server_project_dir,
        'domains'
    )
    env.server_code_dir = os.path.join(
        env.server_project_dir,
        'code',
    )
    env.server_data_dir = os.path.join(
        env.server_project_dir,
        'data',
    )
    env.server_logs_dir = os.path.join(
        env.server_project_dir,
        'logs',
    )
    env.server_db_dir = os.path.join(
        env.server_project_dir,
        'db',
    )
    return env


def ensure_config():
    project = load_project(env.project_name)
    project = project.to_dict()
    # make sure the directories are there!
    run('mkdir -p ' + env.server_project_dir)
    run('mkdir -p ' + env.server_domains_dir)
    run('mkdir -p ' + env.server_code_dir)
    run('mkdir -p ' + env.server_data_dir)
    run('mkdir -p ' + env.server_logs_dir)
    run('mkdir -p ' + env.server_db_dir)

    server_memcached_dir = os.path.join(
        env.server_db_dir,
        'memcached',
    )
    server_redis_dir = os.path.join(
        env.server_db_dir,
        'redis',
    )
    server_postgres_dir = os.path.join(
        env.server_db_dir,
        'postgres',
    )
    server_mongodb_dir = os.path.join(
        env.server_db_dir,
        'mongodb',
    )
    run('mkdir -p ' + server_memcached_dir)
    run('mkdir -p ' + server_redis_dir)
    run('mkdir -p ' + server_postgres_dir)
    run('mkdir -p ' + server_mongodb_dir)

    docker_compose_file = os.path.join(
        env.local_project_dir,
        'docker-compose.yml'
    )
    put(docker_compose_file, env.server_project_dir)
    local_services_dir = os.path.join(
        env.local_project_dir,
        'services',
    )
    put(local_services_dir, env.server_project_dir)
    server_services_dir = os.path.join(
        env.server_project_dir,
        'services',
    )
    run('find ' + server_services_dir + ' -name \'*.sh\' | xargs chmod +x ')
    for domain in project['domains']:
        local_domain_dir = os.path.join(
            env.local_project_dir,
            'domains',
            domain['name']
        )
        put(local_domain_dir, env.server_domains_dir)
        server_domain_dir = os.path.join(
            env.server_domains_dir,
            domain['name'],
        )
        local_certs_dir = os.path.join(
            local_domain_dir,
            'certs',
        )
        put(local_certs_dir, server_domain_dir)
        server_services_dir = os.path.join(
            env.server_domains_dir,
            domain['name'],
            'services',
        )
        run('mkdir -p ' + server_services_dir)
        for service in domain['services']:
            local_service_dir = os.path.join(
                local_domain_dir,
                'services',
                service['name']
            )
            put(local_service_dir, server_services_dir)
            server_service_dir = os.path.join(
                server_services_dir,
                service['name']
            )
            run('chmod -R +x ' + server_service_dir + '/*.{sh,env}')
            server_code_dir = os.path.join(
                env.server_code_dir,
                domain['name'],
                service['name']
            )
            server_data_dir = os.path.join(
                env.server_data_dir,
                domain['name'],
                service['name']
            )
            server_logs_dir = os.path.join(
                env.server_logs_dir,
                domain['name'],
                service['name']
            )
            run('mkdir -p ' + server_code_dir)
            run('mkdir -p ' + server_data_dir)
            run('mkdir -p ' + server_logs_dir)
        server_apps_dir = os.path.join(
            env.server_domains_dir,
            domain['name'],
            'apps',
        )
        run('mkdir -p ' + server_apps_dir)
        for app in domain['apps']:
            local_app_dir = os.path.join(
                local_domain_dir,
                'apps',
                app['name']
            )
            put(local_app_dir, server_apps_dir)
            server_app_dir = os.path.join(
                server_apps_dir,
                app['name']
            )
            run('chmod -R +x ' + server_app_dir + '/*.{sh,env}')
            server_code_dir = os.path.join(
                env.server_code_dir,
                domain['name'],
                app['name']
            )
            server_data_dir = os.path.join(
                env.server_data_dir,
                domain['name'],
                app['name']
            )
            server_logs_dir = os.path.join(
                env.server_logs_dir,
                domain['name'],
                app['name']
            )
            run('mkdir -p ' + server_code_dir)
            run('mkdir -p ' + server_data_dir)
            run('mkdir -p ' + server_logs_dir)


@task
def deploy():
    '''
    Execute as:
    fab using_project:<project-name> deploy
    '''
    # env = using_project(project_name)
    ensure_config()


@task
def remove():
    '''
    Execute as:
    fab using_project:<project-name> remove
    '''
    with cd(env.project_name):
        run('docker-compose down ')  # --remove-orphans')
        run('docker-compose rm --all -f -v')
    run('sudo rm -Rf ' + env.project_name)


# Docker-compose command wrappers


@task
def dc_up(options='', service_name=''):
    '''
    Builds, (re)creates, starts and attaches to containers for a service.
    Execute as:
    fab using_project:<project-name> dc_up:<options>,<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose up ' + options + ' ' +
            service_name)


@task
def dc_ps(service_name=''):
    '''
    Lists containers.
    Execute as:
    fab using_project:<project-name> dc_ps:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose ps ' +
            service_name)


@task
def dc_logs(options='', service_name=''):
    '''
    Displays log output from services.
    Execute as:
    fab using_project:<project-name> dc_log:<options>,<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose logs ' + options + ' ' +
            service_name)


@task
def dc_rm(service_name=''):
    '''
    Removes a stopped container
    Execute as:
    fab using_project:<project-name> dc_rm:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose rm -f -v ' +
            service_name)


@task
def dc_down(options=''):
    '''
    Stops containers and removes containers, networks, volumes, and images \
    created by up.
    Execute as:
    fab using_project:<project-name> dc_down
    '''
    with cd(env.project_name):
        run('docker-compose down ' + options)  # --remove-orphans')


@task
def docker(cmd=''):
    '''
    Execute docker command <cmd>
    '''
    run('docker ' + cmd)


@task
def dc_build(service_name=''):
    '''
    Rebuild service after changing its Dockerfile or its build directory
    Execute as:
    fab using_project:<project-name> dc_build:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose build ' + service_name)


@task
def list_volumes():
    run('docker volume ls')


@task
def volume_ids():
    run('for x in $(docker ps -qa |' +
        ' sed \'1d\'); do ' +
        'docker inspect -f \'{{ .Volumes }}\' ${x}; done')


@task
def rm_dangling_volumes():
    run('docker volume rm $(docker volume ls -qf dangling=true)')


@task
def dc_stop(service_name=''):
    '''
    Stops running containers for a service without removing them
    Execute as:
    fab using_project:<project-name> dc_stop:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose stop ' + service_name)


@task
def dc_kill(service_name=''):
    '''
    Forces running containers for a service to stop by sending them SIGKILL
    Execute as:
    fab using_project:<project-name> dc_kill:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose kill ' + service_name)


@task
def dc_start(service_name=''):
    '''
    Starts existing containers for a service
    Execute as:
    fab using_project:<project-name> dc_start:<service_name>
    '''
    with cd(env.project_name):
        run('docker-compose start ' + service_name)


@task
def dc_run(options='', service_name='', cmd=''):
    '''
    Runs a one-time command against a service.
    Execute as:
    fab using_project:<project-name> dc_run:<options>,<service_name>,<cmd>
    '''
    with cd(env.project_name):
        # run('docker ps -q | xargs docker rm -f')
        run('docker-compose run ' + options + ' ' + service_name + ' ' + cmd)


@task
def dc_restart(service_name='', cmd=''):
    '''
    Restarts a service, executing optional command before restart
    Execute as:
    fab using_project:<project-name> dc_restart:<service_name>[,<cmd>]
    '''
    with settings(warn_only=True):
        dc_stop(service_name=service_name)
        dc_rm(service_name=service_name)
        rm_dangling_volumes()
        if cmd is not None and cmd != '':
            dc_run(options='', service_name=service_name, cmd=cmd)
        dc_up(options='-d', service_name=service_name)
        dc_logs(options='-f', service_name=service_name)


@task
@runs_once
def register_opbeat_deployment(domain_name, app_name):
    '''
    Registers an application's release with opbeat.com
    '''
    project = load_project(env.project_name)
    project = project.to_dict()
    app = get_app(project, domain_name, app_name)
    organization_id = app['env']['DJANGO_OPBEAT_ORGANIZATION_ID']
    app_id = app['env']['DJANGO_OPBEAT_APP_ID']
    secret_token = app['env']['DJANGO_OPBEAT_SECRET_TOKEN']
    code_dir = project['deploy']['server']['code_dir']
    project_path = app['django']['project']['path']
    git_path = os.path.join(
        code_dir,
        domain_name,
        app_name,
        project_path,
    )
    with cd(git_path):
        revision = run(
            'git log -n 1 --pretty="format:%H"'
        )
        branch = run(
            'git rev-parse --abbrev-ref HEAD'
        )
        curl_cmdline = (
            'curl https://intake.opbeat.com/api/v1/organizations/{}'
            '/apps/{}'
            '/releases/'
            ' -H "Authorization: Bearer {}"'
            ' -d rev="{}"'
            ' -d branch="{}"'
            ' -d status=completed'
        ).format(
            organization_id.strip(),
            app_id.strip(),
            secret_token.strip(),
            revision.strip(),
            branch.strip(),
        )
        print(curl_cmdline)
        run(curl_cmdline)
