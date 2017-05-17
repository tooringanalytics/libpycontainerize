#!/bin/bash

# Various important paths
CODE_DIR="{{ project.deploy.docker.code_dir }}"
CONFIG_DIR="{{ project.deploy.docker.config_dir }}"
CERTS_DIR="{{ project.deploy.docker.certs_dir }}"
DATA_DIR="{{ project.deploy.docker.data_dir }}"
LOGS_DIR="{{ project.deploy.docker.logs_dir }}"
PROJECT_DIR="${CODE_DIR}/{{ service.start.root_dir }}"

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
    echo "Executing Command ${cmd} as user {{ service.proc.user }} in directory `pwd`"
    cdproj
    sudo -u {{ service.proc.user }} ${CONFIG_DIR}/__execcmd__.sh ${cmd}
}


function start_service {
    cdproj
    echo "Starting {{ service.name }}..."
    execute_command "{{ service.start.start_cmd }}"
}


function process_cmd {

    # Now execute the command asked.

    case "$@" in
        "start")
            start_service
            ;;
        *)
            execute_command "$@"
            ;;
    esac;
}

createuser
process_cmd "$@"
