FROM docker/compose
WORKDIR /code
COPY . .
CMD ["docker-compose", "up"]