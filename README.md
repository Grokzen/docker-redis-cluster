# docker-redis-cluster

[![Docker Stars](https://img.shields.io/docker/stars/grokzen/redis-cluster.svg)](https://hub.docker.com/r/grokzen/redis-cluster/)
[![Docker Pulls](https://img.shields.io/docker/pulls/grokzen/redis-cluster.svg)](https://hub.docker.com/r/grokzen/redis-cluster/)
[![Build Status](https://travis-ci.org/Grokzen/docker-redis-cluster.svg?branch=master)](https://travis-ci.org/Grokzen/docker-redis-cluster)

Docker image with redis built and installed from source and a cluster is built.


## What this repo and container IS

This repo exists as a resource to make it quick and simple to get a redis cluster up and running with no fuzz or issues with mininal effort. The primary use for this container is to get a cluster up and running in no time that you can use for demo/presentation/development. It is not intended or built for anything else.

I also aim to have every single release of redis that supports a cluster available for use so you can run the exact version you want.

I personally use this to develop redis cluster client code https://github.com/Grokzen/redis-py-cluster


## What this repo and container IS NOT

This container that i have built is not supposed to be some kind of production container or one that is used within any envrionment other then running locally on your machine. It is not ment to be run on kubernetes or in any other prod/stage/test/dev envrionment as a fully working commponent in that envrionment. If that works for you and your use-case then awesome. But this container will not change to fit any other primary solution then to be used locally on your machine.

If you are looking for something else or some production quality or kubernetes compatible solution then you are looking in the wrong repo. There is other projects or forks of this repo that is compatible for that situation/solution.

For all other purposes other then what has been stated you are free to fork and/or rebuild this container using it as a template for what you need.


## Redis instances inside the container

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

If the flag `-e "STANDALONE=true"` is passed there is 2 standalone instances runnin on port 7006 and 7007.

If the flag `-e "SENTINEL=true"` is passed there are 3 Sentinel nodes running on ports 5000 to 5002 matching cluster's master instances.


This image requires at least `Docker` version 1.10 but the latest version is recommended.



# Important for Mac users

If you are using this container to run a redis cluster on your mac computer, then you need to configure the container to use another IP address for cluster discovery as it can't use the default discovery IP that is hardcoded into the container.

If you are using the docker-compose file to build the container, then you must export a envrionment variable on your machine before building the container.

```
# This will make redis do cluster discovery and bind all nodes to ip 127.0.0.1 internally

export REDIS_CLUSTER_IP=0.0.0.0
```

If you are downloading the container from dockerhub, you must add the internal IP envrionment variable to your `docker run` command.

```
docker run  -e "IP=0.0.0.0" grokzen/redis-cluster:latest ...
```



# Usage

To build your own image run:

    make build

To run the container run:

    make up

To stop the container run:

    make down

To connect to your cluster you can use the redis-cli tool:

    redis-cli -c -p 7000

Or the built redis-cli tool inside the container that will connect to the cluster inside the container

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


## Change number of nodes

Be default, it is going to launch 3 masters with 1 slave per master. This is configurable through a number of environment variables:

| Environment variable | Default |
| -------------------- |--------:|
| `INITIAL_PORT`       |    7000 |
| `MASTERS`            |       3 |
| `SLAVES_PER_MASTER`  |       1 | 

Therefore, the total number of nodes (`NODES`) is going to be `$MASTERS * ( $SLAVES_PER_MASTER  + 1 )` and ports are going to range from `$INITIAL_PORT` to `$INITIAL_PORT + NODES - 1`.

At the docker-compose provided by this repository, ports 7000-7050 are already mapped to the hosts'. Either if you need more than 50 nodes in total or if you need to change the initial port number, you should override those values.

Also note that the number of sentinels (if enabled) is the same as the number of masters. The docker-compose file already maps ports 5000-5010 by default. You should also override those values if you have more than 10 masters.

      version: '2'
      services:
        redis-cluster:
          ...
        environment:
          INITIAL_PORT: 9000,
          MASTERS: 2,
          SLAVES_PER_MASTER: 2


## Build alternative redis versions

For a release to be buildable it needs to be present at this url: http://download.redis.io/releases/


### docker build

To build a different redis version use the argument `--build-arg` argument.

    # Example plain docker
    docker build --build-arg redis_version=4.0.13 -t grokzen/redis-cluster .


### docker-compose

To build a different redis version use the `--build-arg` argument.

    # Example docker-compose
    docker-compose build --build-arg "redis_version=4.0.13" redis-cluster



# Available tags

The following tags with pre-built images is available on `docker-hub`.

Latest release in the most recent stable branch will be used as `latest` version.

- latest == 5.0.5

Redis 5.0.x version:

- 5.0.5
- 5.0.4
- 5.0.3
- 5.0.2
- 5.0.1
- 5.0.0

Redis 4.0.x versions:

- 4.0.14
- 4.0.13
- 4.0.12
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

- 3.2.13
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
