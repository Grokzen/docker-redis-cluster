# Redis-cluster

Forked from [docker-redis-cluster](https://github.com/Grokzen/docker-redis-cluster)

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


## Redis instances inside the container

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

If the flag `-e "SENTINEL=true"` is passed there are 3 Sentinel nodes running on ports 5000 to 5002 matching cluster's master instances.

This image requires at least `Docker` version 1.10 but the latest version is recommended.


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
|----------------------|--------:|
| `INITIAL_PORT`       |    7000 |
| `MASTERS`            |       3 |
| `SLAVES_PER_MASTER`  |       0 | 
| `IP`                 | 0.0.0.0 | 

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
    docker run -e "IP=::1" -e "BIND_ADDRESS=::" --network host himadieievsv/redis-cluster:latest


## Build alternative redis versions

For a release to be buildable it needs to be present at this url: http://download.redis.io/releases/


### docker build

To build a different redis version use the argument `--build-arg` argument.

    # Example plain docker
    docker build --build-arg redis_version=6.0.11 -t himadieievsv/redis-cluster .


### docker-compose

To build a different redis version use the `--build-arg` argument.

    # Example docker-compose
    docker-compose build --build-arg "redis_version=6.0.11" redis-cluster


Redis 7.0.x version:

- 7.0.10

# License

This repo is using the MIT LICENSE.

You can find it in the file [LICENSE](LICENSE)
