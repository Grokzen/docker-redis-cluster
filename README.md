# docker-redis-cluster

##### Quick Note

This is a fork of Grokzen's [docker-redis-cluster](https://github.com/Grokzen/docker-redis-cluster) which attempts
to strip down some unneeded config and other improvements that make it more useful for a test setup.

There are few key differences between this docker config and Grokzen's, namely:
  * Removed extra 2 standalone redis instances (ports 7006, 7007) 
  * Advertise IP address matching `eth1` device so that clients connecting from outside with a host networking docker setup can properly redirect to other nodes in the cluster
  * Allow redis version to be passed in as build arg

# Introduction

Docker image with redis built and installed from source.

The main usage for this container is to test redis cluster code. For example in https://github.com/Grokzen/redis-py-cluster repo.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

The image will build the tag `3.2.3` from the redis git repo unless specified otherwise.

The compose file uses v2 formatting for build arg support, so Compose 1.6.0+
and Docker Engine 1.10.0+ is required.


# Available tags

The following tags with pre-built images is available on `docker-hub`. They are based on the tags in this repo.

  * Latest  (Is the highest tag that currently exists in the redis repo [3.2.3 currently])
  * 3.2.3 (Currently the same as 'Latest')


# Build (optional)

To build the image, `docker-compose -f compose.yml build`. By default, this will use redis 3.2.3 and will not tag the resulting image.

To specify an alternate redis version (and with optional tagging):

```
docker build --build-arg VERSION=3.2.2 -t <user>/redis-cluster:3.2.2 .
```

Start the image after building with `docker-compose -f compose.yml up`. Add `-d` to run the server in background/detached mode.


# Run

You have a few options for running the image:
  * If you skipped building, download the latest build from docker hub with `docker pull druotic/redis-cluster:3.2.3` and run it with `docker run -i -t druotic/redis-cluster:3.2.3`.
  * If built using docker-compose, run `docker-compose -f compose.yml up`
  * If build using docker, run `docker run <user>/redis-cluster:3.2.2`
  * 



# Known Issues

If you get a error when rebuilding the image that docker can't do dns lookup on `archive.ubuntu.com` then you need to modify docker to use google IPv4 DNS lookups. Read the following link http://dannytsang.co.uk/docker-on-digitalocean-cannot-resolve-hostnames/ and uncomment the line in `/etc/default/docker` and restart your docker daemon and it should be fixed.
