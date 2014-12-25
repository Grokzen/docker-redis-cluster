# docker-redis-cluster

Docker image with redis built and installed from source.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

It also contains 2 standalone instances that is not part of the cluster. They are running on port 7006 & 7007

It will allways build the latest commit in the 3.0 branch  `https://github.com/antirez/redis`



## Setup / Usage

How to setup docker and start the cluster image.

Install `docker` on your system. 1.0 or higher is recommended. Instructions can be found at http://docs.docker.com/en/latest/installation/. It is also reccomended to add the current user to `docker` system group to remove the need to add sudo to each docker call.

Download the latest build from docker hub with `docker pull grokzen/redis-cluster`

To build the image run either `make dbuild` or `make drebuild`. It will be built to the image name `grokzen/redis-cluster`.

To start the image run `make drun`. It will be started in the background. To gain access to the running image you can get a bash session by running `make dbash`.

Test to connect to the cluster with `redis-cli -p 7000`. If you do not want to install a redis server on your host to get access to `redis-cli` you can run a `exec` command to run it inside the docker container. It can be done with `docker exec -it <ContainerID> /redis/src/redis-cli -p 7000` where `<ContainerID>` can be found inside the CID file at `/tmp/grokzen-redis-cluster.cid` or via `docker ps`.
