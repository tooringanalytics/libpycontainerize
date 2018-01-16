#!/bin/bash
set -e
echo "Setting environment"
user=${MONGODB_USER}
group=${MONGODB_GROUP}
uid=${MONGODB_UID}
gid=${MONGODB_GID}

echo "Checking if user ${user} exists"
if [ -z "$(getent passwd ${user})" ]; then
    echo "Creating group ${group}"
    groupadd -g ${gid} ${group}
    echo "Creating user ${user}"
    useradd -u ${uid} -g ${gid} ${user}
fi

if [ "${1:0:1}" = '-' ]; then
    set -- mongod "$@"
fi

# allow the container to be started with `--user`
if [ "$1" = 'mongod' -a "$(id -u)" = '0' ]; then
    echo "Starting up mongodb"
    chown -R ${user} /data/db
    exec gosu ${user} "$BASH_SOURCE" "$@"
fi

if [ "$1" = 'mongod' ]; then
    numa='numactl --interleave=all'
    if $numa true &> /dev/null; then
        set -- $numa "$@"
    fi
fi

echo "Executing command $@"
exec "$@"