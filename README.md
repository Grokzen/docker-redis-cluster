# docker-redis-cluster

Docker image with redis built and installed from source.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

It will allways build the latest commit in the 3.0 branch from redis repo `https://github.com/antirez/redis`.



## Setup / Usage

How to setup docker and start the cluster image.

- Install `docker` on your system. 1.0 or higher is recommended. Instructions can be found at http://docs.docker.com/en/latest/installation/. It is also reccomended to add the current user to `docker` system group to remove the need to add sudo to each docker call.
- Run `make docker-build` or `make docker-rebuild` to build the image. When rebuilding the image, no cached layers will be used.
- Run one of
  
  - `make docker-run` to start the server and tail first redis server (the one creating the cluster)
  - `make docker-run-d` to run it in the background.
  - `make docker-run-interactive` starts `/bin/bash` (good for debugging) [`start.sh` have to be runned manually. No cluster will be created, Supervisord will not start automatically]

- Test to connect to the cluster with `redis-cli -p 7000`. If you do not want to install a redis server on your host to get access to `redis-cli` you can run a `exec` command to run it inside the docker container. It can be done with `docker exec -it <ContainerID> /redis/src/redis-cli -p 7000` where `<ContainerID>` can be found via `docker ps`
