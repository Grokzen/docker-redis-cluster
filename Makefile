help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  docker-build                build the docker image containing a redis cluster"
	@echo "  docker-rebuild              rebuilds the image from scratch without using any cached layers"
	@echo "  docker-run                  run the built docker image"
	@echo "  docker-run-d                run the built docker image"
	@echo "  docker-run-interactive      run the built docker image"
	@echo "  docker-kill                 send stop signal to the running docker instance. do not remove image."
	@echo "  docker-remove               remove the built docker image from you system"

docker-build:
	@echo "Building docker image..."
	docker build -t redis-server .

docker-rebuild:
	@echo "Rebuilding docker image..."
	docker build --no-cache=true -t redis-server .

docker-run:
	@echo "Running docker image..."
	docker run -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -i -t redis-server

docker-run-d:
	@echo "Running docker image in daemon mode..."
	docker run -d -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -i -t redis-server

docker-run-interactive:
	@echo "Running docker image in interactive mode..."
	docker run -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -i -t redis-server /sbin/my_init --enable-insecure-key -- /bin/bash

docker-kill:
	@echo "NYI"

docker-remove:
	@echo "NYI"
