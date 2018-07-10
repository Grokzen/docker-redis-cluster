help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         builds docker-compose containers"
	@echo "  up            starts docker-compose containers"
	@echo "  down          stops the running docker-compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"
	@echo "  bash          starts bash inside a running container."
	@echo "  cli           run redis-cli inside the container on the server with port 7000"
	@echo " ---------"
	@echo "Bulk build options"
	@echo "  build-3.0"
	@echo "  build-3.2"
	@echo "  build-4.0"
	@echo "  build-5.0"
	@echo "  push-releases"

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

build-3.0:
	docker build --build-arg redis_version=3.0.0 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.0
	docker build --build-arg redis_version=3.0.1 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.1
	docker build --build-arg redis_version=3.0.2 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.2
	docker build --build-arg redis_version=3.0.3 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.3
	docker build --build-arg redis_version=3.0.4 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.4
	docker build --build-arg redis_version=3.0.5 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.5
	docker build --build-arg redis_version=3.0.6 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.6
	docker build --build-arg redis_version=3.0.7 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.0.7

build-3.2:
	docker build --build-arg redis_version=3.2.0 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.0
	docker build --build-arg redis_version=3.2.1 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.1
	docker build --build-arg redis_version=3.2.2 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.2
	docker build --build-arg redis_version=3.2.3 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.3
	docker build --build-arg redis_version=3.2.4 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.4
	docker build --build-arg redis_version=3.2.5 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.5
	docker build --build-arg redis_version=3.2.6 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.6
	docker build --build-arg redis_version=3.2.7 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.7
	docker build --build-arg redis_version=3.2.8 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.8
	docker build --build-arg redis_version=3.2.9 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.9
	docker build --build-arg redis_version=3.2.10 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.10
	docker build --build-arg redis_version=3.2.11 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:3.2.11

build-4.0:
	docker build --build-arg redis_version=4.0.0 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.0
	docker build --build-arg redis_version=4.0.1 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.1
	docker build --build-arg redis_version=4.0.2 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.2
	docker build --build-arg redis_version=4.0.3 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.3
	docker build --build-arg redis_version=4.0.4 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.4
	docker build --build-arg redis_version=4.0.5 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.5
	docker build --build-arg redis_version=4.0.6 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.6
	docker build --build-arg redis_version=4.0.7 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.7
	docker build --build-arg redis_version=4.0.8 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.8
	docker build --build-arg redis_version=4.0.9 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.9
	docker build --build-arg redis_version=4.0.10 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:4.0.10

build-5.0:
	docker build --build-arg redis_version=5.0-rc1 -t grokzen/redis-cluster .
	docker tag grokzen/redis-cluster grokzen/redis-cluster:5.0-rc1

push-releases:
	docker push grokzen/redis-cluster:3.0.0
	docker push grokzen/redis-cluster:3.0.1
	docker push grokzen/redis-cluster:3.0.2
	docker push grokzen/redis-cluster:3.0.3
	docker push grokzen/redis-cluster:3.0.4
	docker push grokzen/redis-cluster:3.0.5
	docker push grokzen/redis-cluster:3.0.6
	docker push grokzen/redis-cluster:3.0.7
	docker push grokzen/redis-cluster:3.2.0
	docker push grokzen/redis-cluster:3.2.1
	docker push grokzen/redis-cluster:3.2.2
	docker push grokzen/redis-cluster:3.2.3
	docker push grokzen/redis-cluster:3.2.4
	docker push grokzen/redis-cluster:3.2.5
	docker push grokzen/redis-cluster:3.2.6
	docker push grokzen/redis-cluster:3.2.7
	docker push grokzen/redis-cluster:3.2.8
	docker push grokzen/redis-cluster:3.2.9
	docker push grokzen/redis-cluster:3.2.10
	docker push grokzen/redis-cluster:3.2.11
	docker push grokzen/redis-cluster:4.0.0
	docker push grokzen/redis-cluster:4.0.1
	docker push grokzen/redis-cluster:4.0.2
	docker push grokzen/redis-cluster:4.0.3
	docker push grokzen/redis-cluster:4.0.4
	docker push grokzen/redis-cluster:4.0.5
	docker push grokzen/redis-cluster:4.0.6
	docker push grokzen/redis-cluster:4.0.7
	docker push grokzen/redis-cluster:4.0.8
	docker push grokzen/redis-cluster:4.0.9
	docker push grokzen/redis-cluster:4.0.10
	docker push grokzen/redis-cluster:latest
