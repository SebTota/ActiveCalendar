#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=active.sebtota.com \
TRAEFIK_TAG=active.sebtota.com \
STACK_NAME=active-sebtota-com \
TAG=prod \
docker compose \
-f docker-compose.prod.yml \
up -d
