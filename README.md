# docker-redis-cluster

[![Docker Stars](https://img.shields.io/docker/stars/grokzen/redis-cluster.svg)](https://hub.docker.com/r/grokzen/redis-cluster/)
[![Docker Pulls](https://img.shields.io/docker/pulls/grokzen/redis-cluster.svg)](https://hub.docker.com/r/grokzen/redis-cluster/)
[![Build Status](https://travis-ci.org/Grokzen/docker-redis-cluster.svg?branch=master)](https://travis-ci.org/Grokzen/docker-redis-cluster)

Docker image with redis built and installed from source and a cluster is built.

To find all redis-server releases see them here https://github.com/antirez/redis/releases


## Discussions, help, guides

Github have recently released their `Discussions` feature into beta for more repositories across the github space. This feature is enabled on this repo since a while back.

Becuase we now have this feature, the issues feature will NOT be a place where you can now ask general questions or need simple help with this repo and what it provides.

What can you expect to find in there?

 - A place where you can freely ask any question regarding this repo.
 - Ask questions like `how do i do X?`
 - General help with problems with this repo
 - Guides written by me or any other contributer with useful examples and ansers to commonly asked questions and how to resolve thos problems.
 - Approved answers to questions marked and promoted by me if help is provided by the community regarding some questions


## What this repo and container IS

This repo exists as a resource to make it quick and simple to get a redis cluster up and running with no fuzz or issues with mininal effort. The primary use for this container is to get a cluster up and running in no time that you can use for demo/presentation/development. It is not intended or built for anything else.

I also aim to have every single release of redis that supports a cluster available for use so you can run the exact version you want.

I personally use this to develop redis cluster client code https://github.com/Grokzen/redis-py-cluster


## What this repo and container IS NOT

This container that i have built is not supposed to be some kind of production container or one that is used within any environment other than running locally on your machine. It is not ment to be run on kubernetes or in any other prod/stage/test/dev environment as a fully working commponent in that environment. If that works for you and your use-case then awesome. But this container will not change to fit any other primary solution than to be used locally on your machine.

If you are looking for something else or some production quality or kubernetes compatible solution then you are looking in the wrong repo. There is other projects or forks of this repo that is compatible for that situation/solution.

For all other purposes other than what has been stated you are free to fork and/or rebuild this container using it as a template for what you need.


## Redis major version support and docker.hub availability

Starting from `2020-04-01` this repo will only support and make available on docker.hub all minor versions in the latest 3 major versions of redis-server software. At this date the tags on docker.hub for major versions 3.0, 3.2 & 4.0, 5.0 will be removed and only 6.0, 6.2, 7.0 will be available to download. This do not mean that you will not be able to build your desired version from this repo but there is no guarantees or support or hacks that will support this out of the box.

Moving forward when a new major release is shipped out, at the first minor release X.Y.1 version of the next major release, all tags from the last supported major version will be removed from docker.hub. This will give some time for the community to adapt and move forward in the versions before the older major version is removed from docker.hub.

This major version schema support follows the same major version support that redis itself use.


## Redis instances inside the container

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

If the flag `-e "SENTINEL=true"` is passed there are 3 Sentinel nodes running on ports 5000 to 5002 matching cluster's master instances.


This image requires at least `Docker` version 1.10 but the latest version is recommended.



# Important for Mac users

If you are using this container to run a redis cluster on your mac computer, then you need to configure the container to use another IP address for cluster discovery as it can't use the default discovery IP that is hardcoded into the container.

If you are using the docker-compose file to build the container, then you must export a environment variable on your machine before building the container.

```
# This will make redis do cluster discovery and bind all nodes to ip 127.0.0.1 internally

export REDIS_CLUSTER_IP=0.0.0.0
```

If you are downloading the container from dockerhub, you must add the internal IP environment variable to your `docker run` command.

```
docker run -e "IP=0.0.0.0" -p 7000-7005:7000-7005 grokzen/redis-cluster:latest
```



# Usage

This git repo is using `invoke` to pull, build, push docker images. You can use it to build your own images if you like.

The invoke scripts in this repo is written only for python 3.7 and above

Install `invoke` with `pip install invoke`.

This script will run `N num of cpu - 1` parralell tasks based on your version input.

To see available commands run `invoke -l` in the root folder of this repo. Example

```
(tmp-615229a94c330b9) ➜  docker-redis-cluster git:(invoke) ✗ invoke -l
"Configured multiprocess pool size: 3
Available tasks:

  build
  list
  pull
  push
```

Each command is only taking one required positional argument `version`. Example:

```
(tmp-615229a94c330b9) ➜  docker-redis-cluster git:(invoke) ✗ invoke build 7.0
...
```

and it will run the build step on all versions that starts with 6.0.

The only other optional usefull argument is `--cpu=N` and it will set how many paralell processes will be used. By default you will use n - 1 number of cpu cores that is available on your system. Commands like pull and push aare not very cpu intensive so using a higher number here might speed things up if you have good network bandwidth.


## Makefile (legacy)

Makefile still has a few docker-compose commands that can be used

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


## IPv6 support

By default, redis instances will bind and accept requests from any IPv4 network.
This is configurable by an environment variable that specifies which address a redis instance will bind to.
By using the IPv6 variant `::` as counterpart to IPv4s `0.0.0.0` an IPv6 cluster can be created.

| Environment variable | Default |
| -------------------- | ------: |
| `BIND_ADDRESS`       | 0.0.0.0 |

Note that Docker also needs to be [configured](https://docs.docker.com/config/daemon/ipv6/) for IPv6 support.
Unfortunately Docker does not handle IPv6 NAT so, when acceptable, `--network host` can be used.

    # Example using plain docker
    docker run -e "IP=::1" -e "BIND_ADDRESS=::" --network host grokzen/redis-cluster:latest


## Build alternative redis versions

For a release to be buildable it needs to be present at this url: http://download.redis.io/releases/


### docker build

To build a different redis version use the argument `--build-arg` argument.

    # Example plain docker
    docker build --build-arg redis_version=6.0.11 -t grokzen/redis-cluster .


### docker-compose

To build a different redis version use the `--build-arg` argument.

    # Example docker-compose
    docker-compose build --build-arg "redis_version=6.0.11" redis-cluster



# Available tags

The following tags with pre-built images is available on `docker-hub`.

Latest release in the most recent stable branch will be used as `latest` version.

- latest == 7.0.10

Redis 7.0.x version:

- 7.0.10
- 7.0.9
- 7.0.8
- 7.0.7
- 7.0.6
- 7.0.5
- 7.0.4
- 7.0.3
- 7.0.2
- 7.0.1
- 7.0.0

Redis 6.2.x versions:

- 6.2.11
- 6.2.10
- 6.2.9
- 6.2.8
- 6.2.7
- 6.2.6
- 6.2.5
- 6.2.4
- 6.2.3
- 6.2.2
- 6.2.1
- 6.2.0

Redis 6.0.x versions:

- 6.0.18
- 6.0.17
- 6.0.16
- 6.0.15
- 6.0.14
- 6.0.13
- 6.0.12
- 6.0.11
- 6.0.10
- 6.0.9
- 6.0.8
- 6.0.7
- 6.0.6
- 6.0.5
- 6.0.4
- 6.0.3
- 6.0.2
- 6.0.1
- 6.0.0


## Unavailable major versions

The following major versions is no longer available to be downloaded from docker.hub. You can still build and run them directly from this repo.

- 5.0
- 4.0
- 3.2
- 3.0


# License

This repo is using the MIT LICENSE.

You can find it in the file [LICENSE](LICENSE)
