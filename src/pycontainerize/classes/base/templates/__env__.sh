#!/usr/bin/bash

# Service Config and Paths
PROJECT_NAME="{{ project.name }}"
SERVICE_NAME="{{ service.name }}"
CONFIG_DIR={{ project.deploy.docker.config_dir }}
CERTS_DIR={{ project.deploy.docker.certs_dir }}

# export the paths
export PROJECT_NAME
export SERVICE_NAME
export CONFIG_DIR
export CERTS_DIR
