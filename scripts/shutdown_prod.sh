#! /usr/bin/env sh

# Exit in case of error
set -e

docker compose \
-f docker-compose.prod.yml \
down --rmi all --volumes --remove-orphans
