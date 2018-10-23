# docker-redis-cluster

[![Docker Stars](https://img.shields.io/docker/stars/grokzen/redis-cluster.svg)](hub])
[![Docker Pulls](https://img.shields.io/docker/pulls/grokzen/redis-cluster.svg)](hub])

Docker hub: https://hub.docker.com/r/grokzen/redis-cluster/

Docker image with redis built and installed from source.

The main usage for this container is to test redis cluster code. For example in https://github.com/Grokzen/redis-py-cluster repo.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

If the flag `-e "SENTINEL=true"` is passed there are 3 Sentinel nodes running on ports 5000 to 5002 matching cluster's master instances.

It also contains 2 standalone instances that is not part of the cluster. They are running on port 7006 & 7007

This image requires at least `Docker` version 1.10 but the latest version is recommended.

Update 2018-03-06: All images/tags on dockerhub has been rebuilt with the latest code and re-uploaded to dockerhub.


# Note for Mac users

If you are using this container to run a redis cluster on your mac computer, then you need to configure the container to use another IP address for cluster discovery as it can't use the default discovery IP that is hardcoded into the container.

If you are using the docker-compose file to build the container, then you must export a envrionment variable on your machine before building the container.

```
# This will make redis do cluster discovery and bind all nodes to ip 127.0.0.1 internally

export REDIS_CLUSTER_IP=0.0.0.0
```

If you are downloading the container from dockerhub, you must add the internal IP envrionment variable to your `docker run` command.

```
docker run grokzen/redis-cluster:latest -e "IP=0.0.0.0" ...
```



# Usage

To build your own image run:

    make build

And to run the container use:

    make up

    # and top stop the container run

    make down

To connect to your cluster you can use the redis-cli tool:

    redis-cli -c -p 7000

    # or the built redis-cli tool inside the container

    make cli


## Include standalone redis instances

Standalone instances is not enabled by default, but available to use to run 2 standalone redis instances that is not clustered.

If running with plain docker run

    docker run ... -e STANDALONE=true ...

When running with docker-compose, set the envrionment variable on your system `REDIS_USE_STANDALONE=true` and start your container or modify the `docker-compose.yml` file

      version: '2'
      services:
        redis-cluster:
          ...
        environment:
          STANDALONE: 'true'


## Include sentinel instances

Sentinel instances is not enabled by default.

If running with plain docker send in `-e SENTINEL=true`.

When running with docker-compose set the environment variable on your system `REDIS_USE_SENTINEL=true` and start your container.

      version: '2'
      services:
        redis-cluster:
          ...
        environment:
          SENTINEL: 'true'


## Build alternative redis versions

For a release to be buildable it needs to be present at this url: http://download.redis.io/releases/


### docker build

To set a different redis version use the argument --build-arg

    # Example
    docker build --build-arg redis_version=3.2.0 -t grokzen/redis-cluster .


### docker-compose

To set a different redis version you must change the variable 'redis_version' inside the docker-compose file.

Then you simply rebuild the compose file and it should be updated with the desired redis version.


# Available tags

The following tags with pre-built images is available on `docker-hub`.

Latest release in the most recent stable branch will be used as `latest` version.

- latest == 5.0.0

Redis 5.0.x version:

- 5.0.0

Redis 4.0.x versions:

- 4.0.11
- 4.0.10
- 4.0.9
- 4.0.8
- 4.0.7
- 4.0.6
- 4.0.5
- 4.0.4
- 4.0.3
- 4.0.2
- 4.0.1
- 4.0.0

Redis 3.2.x versions:

- 3.2.12
- 3.2.11
- 3.2.10
- 3.2.9
- 3.2.8
- 3.2.7
- 3.2.6
- 3.2.5
- 3.2.4
- 3.2.3
- 3.2.2
- 3.2.1
- 3.2.0

Redis 3.0.x versions:

- 3.0.7
- 3.0.6
- 3.0.5
- 3.0.4
- 3.0.3
- 3.0.2
- 3.0.1
- 3.0.0


# License

This repo is using the MIT LICENSE.

You can find it in the file [LICENSE](LICENSE)
