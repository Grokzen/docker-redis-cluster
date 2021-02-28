help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         builds docker-compose containers"
	@echo "  up            starts docker-compose containers"
	@echo "  down          stops the running docker-compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"
	@echo "  bash          starts bash inside a running container."
	@echo "  cli           run redis-cli inside the container on the server with port 7000"

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose stop

rebuild:
	docker-compose build --no-cache

bash:
	docker-compose exec redis-cluster /bin/bash

cli:
	docker-compose exec redis-cluster /redis/src/redis-cli -p 7000
