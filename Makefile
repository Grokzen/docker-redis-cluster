help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "Docker Compose commands:"
	@echo "  build         builds docker compose containers"
	@echo "  up            starts docker compose containers"
	@echo "  down          stops the running docker compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"
	@echo "  bash          starts bash inside a running container."
	@echo "  cli           run redis-cli inside the container on the server with port 7000"
	@echo ""
	@echo "Invoke tasks:"
	@echo "  pull          pull Redis Docker images (use VERSION and CPU variables)"
	@echo "  build-images  build Redis Docker images (use VERSION and CPU variables)"
	@echo "  push          push Redis Docker images (use VERSION and CPU variables)"
	@echo "  list          list all available Redis versions"
	@echo "  list-releases list Redis releases from GitHub"

# Default values
CPU ?= 2

build:
	docker compose build

up:
	docker compose up

down:
	docker compose stop

rebuild:
	docker compose build --no-cache

bash:
	docker compose exec redis-cluster /bin/bash

cli:
	docker compose exec redis-cluster /redis/src/redis-cli -p 7000

# Invoke tasks
pull:
	invoke pull --version $(VERSION) --cpu $(CPU)

build-images:
	invoke build --version $(VERSION) --cpu $(CPU)

push:
	invoke push --version $(VERSION) --cpu $(CPU)

list:
	invoke list

list-releases:
	invoke list-releases
