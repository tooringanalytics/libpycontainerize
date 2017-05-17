#!/bin/bash

# Various important paths
CODE_DIR="{{ project.deploy.docker.code_dir }}"
CONFIG_DIR="{{ project.deploy.docker.config_dir }}"
CERTS_DIR="{{ project.deploy.docker.certs_dir }}"
DATA_DIR="{{ project.deploy.docker.data_dir }}"
VIRTUALENV_DIR="{{ project.deploy.docker.code_dir }}/venv"
LOGS_DIR="{{ project.deploy.docker.logs_dir }}"
PROJECT_DIR="${CODE_DIR}/{{ service.start.root_dir }}"
REQUIREMENTS_FILE="${PROJECT_DIR}/{{ service.start.requirements }}"

# Repository settings
REPO_KEY="${CERTS_DIR}/{{ service.git.login_key_priv }}"
GIT_URL='{{ service.git.url }}'
REPO_NAME="{{ service.git.repo_name }}"
BRANCH_NAME="{{ service.git.branch }}"

# Service settings
SERVICE_NAME="{{ service.name }}"
PROJECT_NAME="{{ project.name }}"

# Environment variables
{% for envar, value in service.env.iteritems() %}
{{ envar }}='{{ value }}'
export {{ envar }}
{% endfor %}


function cdproj {
    cd ${PROJECT_DIR}
}


function setperms {

    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} ${CODE_DIR}
    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} ${LOGS_DIR}
    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} ${CONFIG_DIR}
    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} ${DATA_DIR}

    # Make all directories user & group read/writeable/statable(x)
    chmod ug+rwx ${CODE_DIR} ${LOGS_DIR} ${CONFIG_DIR} ${DATA_DIR}
    # Make all directories readable and statable for everyone else
    chmod a+rx ${CODE_DIR} ${LOGS_DIR} ${CONFIG_DIR} ${DATA_DIR}
    # Make everything inside code dir user read/writeable
    chmod -R ug+w ${CODE_DIR}
    # Make everything inside code dir readable for everyone else
    chmod -R a+r ${CODE_DIR}
    # Make everything inside logs dir readable & writeable for everyone else
    chmod -R a+rw ${LOGS_DIR}
    # Make everything inside config dir readable for everyone else
    chmod -R a+r ${CONFIG_DIR}
    sync
}


function createuser {
    echo "Creating service user and group"
    groupadd -g {{ service.proc.gid }} {{ service.proc.user }}
    useradd -u {{ service.proc.uid }} -g {{ service.proc.gid }} {{ service.proc.user }}
    setperms
}

function execute_command {
    cmd="$@"
    echo "Executing Command ${cmd} as user {{ service.proc.user }}"

    sudo -u {{ service.proc.user }} ${CONFIG_DIR}/exec_cmd_wrapper.sh ${cmd}
}

function start_supervisord {
    # setup config for supervisord
    echo "Starting Supervisord"
    if [ ! -f /etc/supervisor/conf.d/supervisor-service.conf ]; then
        mkdir -p /etc/supervisor/conf.d
        ln -s ${CONFIG_DIR}/supervisor-service.conf /etc/supervisor/conf.d/
        cp ${CONFIG_DIR}/supervisord.conf /etc/supervisor
    fi;
    mkdir -p /var/log/supervisor
    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} /var/log/supervisor
    mkdir -p /opt/supervisor
    chown -R {{ service.proc.uid }}:{{ service.proc.gid }} /opt
    sudo -u {{ service.proc.user }} supervisord -u {{ service.proc.uid }} -c /etc/supervisor/supervisord.conf -n -e debug
}


function init_git_ssh {
    # Set up the SSH keys for the git remote repository
    # chmod 600 ${CONFIG_DIR}/repo-key && \
    #     echo "IdentityFile ${CONFIG_DIR}/repo-key" >> /etc/ssh/ssh_config && \
    #     echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    #     cat /etc/ssh/ssh_config
    echo "Setting up SSH keys for the Git Server."
    # rm -f /etc/ssh/ssh_config
    # touch /etc/ssh/ssh_config
    chmod 664 ${REPO_KEY}
    echo "IdentityFile ${REPO_KEY}" >> /etc/ssh/ssh_config
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
    cat /etc/ssh/ssh_config
}


function update_venv {
    # Now install the python dependencies.
    echo "Installing the project's python dependencies"
    if [ ! -f ${CODE_DIR}/venv/bin/activate ]; then
        echo "Virtualenv not found."
        return
    fi;
    source ${CODE_DIR}/venv/bin/activate
    pip install --upgrade pip
    pip install -r ${REQUIREMENTS_FILE}
    setperms
}


function ensure_venv {
    # ensure there is a virtualenv for the service
    echo "Ensuring virtualenv"
    if [ ! -f ${CODE_DIR}/venv/bin/activate ]; then
        echo "Creating virtualenv."
        pip install --upgrade virtualenv
        virtualenv ${CODE_DIR}/venv
        setperms
        update_venv
    fi;
}

function load_venv {
    ensure_venv
    # Load the virtualenv and upgrade pip.
    echo "Loading virtualenv."
    source ${CODE_DIR}/venv/bin/activate
}

function ensure_git_repo {
    # Clone the django project
    init_git_ssh
    if [ ! -d ${PROJECT_DIR} ]; then
        echo "Cloning Repository"
        git clone ${GIT_URL} ${PROJECT_DIR}
        mkdir -p ${PROJECT_DIR}/static
        mkdir -p ${PROJECT_DIR}/staticfiles
        mkdir -p ${PROJECT_DIR}/mediafiles
        setperms
        update_venv
    fi;
}

function update_git_repo {
    ensure_git_repo
    echo "Updating Repository"
    cdproj
    git fetch origin
    git checkout ${BRANCH_NAME}
    git merge origin/${BRANCH_NAME}
    setperms
    update_venv
}

function custom_cmd {
    cdproj
    echo "Executing command $@ in directory `pwd`"
    execute_command "$@"
}

function start_service {
    cdproj
    # Start off all servers...
    echo "Starting Service"
    echo `pwd`
    # start_supervisord
    execute_command "{{ service.start.start_cmd }}"
}


function process_cmd {

    # Now execute the command asked.
    export DJANGO_SECRET_KEY

    case "$@" in
        "ensure_venv")
            ensure_venv
            ;;
        "update_repo")
            load_venv
            update_git_repo
            ;;
        "start")
            ensure_git_repo
            load_venv
            start_service
            ;;
        *)
            ensure_git_repo
            load_venv
            custom_cmd "$@"
            ;;
    esac;
}

createuser
process_cmd "$@"
