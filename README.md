# docker-redis-cluster

Docker image with redis built and installed from source.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

It also contains 2 standalone instances that is not part of the cluster. They are running on port 7006 & 7007

It will allways build the latest commit in the 3.0 branch  `https://github.com/antirez/redis/tree/3.0`



# Setup Docker

How to setup docker and start the cluster image.

Install `docker` on your system. 1.0 or higher is recommended. Instructions can be found at http://docs.docker.com/en/latest/installation/. It is also reccomended to add the current user to `docker` system group to remove the need to add sudo to each docker call.



# Usage

If you want to use `docker-compose (fig)` please read next section.

Download the latest build from docker hub with `docker pull grokzen/redis-cluster`

To build the image run either `make build` or `make rebuild`. It will be built to the image name `grokzen/redis-cluster`.

To start the image run `make run`. It will be started in the background. To gain access to the running image you can get a bash session by running `make bash`.

Test to connect to the cluster with `redis-cli -p 7000`. If you do not want to install a redis server on your host to get access to `redis-cli` you can run a `exec` command to run it inside the docker container. It can be done with `docker exec -it <ContainerID> /redis/src/redis-cli -p 7000` where `<ContainerID>` can be found inside the CID file at `/tmp/grokzen-redis-cluster.cid` or via `docker ps`.



# Docker compose (fig)

This image contains a `compose.yml` file that can be used with `docker-compose (fig)` to run the image. Docker compose is simpler to use then the old `Makefile`.

Build the image with `docker-compose -f compose.yml build`.

Start the image after building with `docker-compose -f compose.yml up`. Add `-d` to run the server in background/detatched mode.



# Known Issues

If you get a error when rebuilding the image that docker can't do dns lookup on `archive.ubuntu.com` then you need to modify docker to use google IPv4 DNS lookups. Read the following link http://dannytsang.co.uk/docker-on-digitalocean-cannot-resolve-hostnames/ and uncomment the line in `/etc/default/docker` and restart your docker daemon and it should be fixed.
