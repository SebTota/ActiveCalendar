#! /usr/bin/env sh

# Exit in case of error
set -e

docker compose \
-f docker-compose.dev.yml \
up -d