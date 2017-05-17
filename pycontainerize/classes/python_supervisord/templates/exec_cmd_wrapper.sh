#!/bin/bash
CODE_DIR="{{ project.deploy.docker.code_dir }}"

cmd="$@"
echo "exec_cmd_wrapper.sh: Executing command ${cmd}"

# Go to project root dir
directory="${CODE_DIR}/{{ service.start.root_dir }}"
cd ${directory}

# Environment variables
{% for envar, value in service.env.iteritems() %}
{{ envar }}='{{ value }}'
export {{ envar }}
{% endfor %}

echo "Loading virtualenv."
source ${CODE_DIR}/venv/bin/activate

${cmd}
