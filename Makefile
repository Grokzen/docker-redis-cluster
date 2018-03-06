CID_FILE = /tmp/grokzen-redis-cluster.cid
CID =`cat $(CID_FILE)`
IMAGE_NAME = grokzen/redis-cluster
PORTS = -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -p 7006:7006 -p 7007:7007

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build           build the docker image containing a redis cluster"
	@echo "  rebuild         rebuilds the image from scratch without using any cached layers"
	@echo "  run             run the built docker image"
	@echo "  bash            starts bash inside a running container."
	@echo "  clean           removes the tmp cid file on disk"
	@echo "  cli             run redis-cli inside the container on the server with port 7000"
	@echo " ---------"
	@echo "Docker compose commands"
	@echo "  compose-build   builds docker-compose containers"
	@echo "  compose-up      starts docker-compose containers"
	@echo "  compose-stop    stops the running docker-compose containers"
	@echo " ---------"
	@echo "Bulk build options"
	@echo "  build-3.0"
	@echo "  build-3.2"
	@echo "  build-4.0"
	@echo "  push-releases"

build:
	@echo "Building docker image..."
	docker build -t ${IMAGE_NAME} .

rebuild:
	@echo "Rebuilding docker image..."
	docker build --no-cache=true -t ${IMAGE_NAME} .

run:
	@echo "Running docker image..."
	docker run -d $(PORTS) --cidfile $(CID_FILE) -i -t ${IMAGE_NAME}

bash:
	docker exec -it $(CID) /bin/bash

stop:
	docker stop $(CID)
	-make clean

clean:
	# Cleanup cidfile on disk
	-rm $(CID_FILE)

cli:
	docker exec -it $(CID) /redis/src/redis-cli -p 7000

compose-build:
	docker-compose -f docker-compose.yml build

compose-up:
	docker-compose -f docker-compose.yml up

compose-stop:
	docker-compose -f docker-compose.yml stop

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
