#!/bin/bash
# docker-entrypoint.sh is 'burned' into the image
# it should be used to call all user-definable
# actions.


. /home/docker/config/server.env


/home/docker/config/configure-app.sh "$@"
