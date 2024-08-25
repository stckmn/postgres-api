#!/bin/bash

# ./scripts/run-dev.sh
# Starts the dev environment
# Stops the docker environment if SIGINT or killed

# Exit script immediately if any command returns a non-zero exit status
set -e

# Pass any command line args into a single variable
DOCKER_ARGS="$*"

# call ctrl_c on <C>-c or kill command
trap ctrl_c SIGINT
trap ctrl_c SIGTERM

function ctrl_c () {
    echo "Gracefully shutting down containers ..."
    docker compose --profile dev down --volumes
    exit 0
}

# The main reason for this script
docker compose --profile dev up $DOCKER_ARGS
