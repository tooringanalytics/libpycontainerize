#!/bin/bash
CODE_DIR="{{ project.deploy.docker.code_dir }}"
CONFIG_DIR="{{ project.deploy.docker.config_dir }}"

cmd="$@"
echo "__exec__.sh: Executing command ${cmd}"

# Go to project root dir
directory="${CODE_DIR}/{{ service.start.root_dir }}"
cd ${directory}

# Environment variables
{% for envar, value in service.env.iteritems() %}
{{ envar }}='{{ value }}'
export {{ envar }}
{% endfor %}

# Execute the command
${CONFIG_DIR}/__precmd__.sh
${cmd}
${CONFIG_DIR}/__postcmd__.sh
