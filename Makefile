CID_FILE = /tmp/grokzen-redis-cluster.cid
CID =`cat $(CID_FILE)`
IMAGE_NAME = grokzen/redis-cluster
PORTS = -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -p 7006:7006 -p 7007:7007

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  dbuild           build the docker image containing a redis cluster"
	@echo "  drebuild         rebuilds the image from scratch without using any cached layers"
	@echo "  drun             run the built docker image"
	@echo "  dbash            starts bash inside a running container."
	@echo "  dclean           removes the tmp cid file on disk"

dbuild:
	@echo "Building docker image..."
	docker build -t ${IMAGE_NAME} .

drebuild:
	@echo "Rebuilding docker image..."
	docker build --no-cache=true -t ${IMAGE_NAME} .

drun:
	@echo "Running docker image..."
	docker run -d $(PORTS) --cidfile $(CID_FILE) -i -t ${IMAGE_NAME}

dbash:
	docker exec -it $(CID) /bin/bash

dstop:
	docker stop $(CID)
	-make dclean

dclean:
	# Cleanup cidfile on disk
	-rm $(CID_FILE)
