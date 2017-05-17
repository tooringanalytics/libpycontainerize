#!/usr/bin/bash

# Service Config and Paths
REPO_NAME="{{ service.git.repo_name }}"
PROJECT_NAME="{{ project.name }}"
SERVICE_NAME="{{ service.name }}"
BRANCH_NAME="{{ service.git.branch }}"
CONFIG_DIR={{ project.deploy.docker.config_dir }}
CERTS_DIR={{ project.deploy.docker.certs_dir }}
VIRTUALENV_DIR={{ project.deploy.docker.code_dir }}/venv
GIT_URL='{{ service.git.url }}'

export REPO_NAME
export PROJECT_NAME
export SERVICE_NAME
export BRANCH_NAME
export CONFIG_DIR
export CERTS_DIR
export VIRTUALENV_DIR
export GIT_URL
