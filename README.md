# docker-redis-cluster

[![Docker Stars](https://img.shields.io/docker/stars/grokzen/redis-cluster.svg)](hub])
[![Docker Pulls](https://img.shields.io/docker/pulls/grokzen/redis-cluster.svg)](hub])

Docker image with redis built and installed from source.

The main usage for this container is to test redis cluster code. For example in https://github.com/Grokzen/redis-py-cluster repo.

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7000 to 7005.

It also contains 2 standalone instances that is not part of the cluster. They are running on port 7006 & 7007

This image requires at least `Docker` version 1.10 but the latest version is recommended.



# Available tags

The following tags with pre-built images is available on `docker-hub`.

- latest == 3.2.9

For redis 4.0 versions please see the branch 'redis-4.0'

Redis 3.2.x versions:

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
- 3.2-rc1

Redis 3.0.x versions:

- 3.0.7
- 3.0.6
- 3.0.5
- 3.0.4
- 3.0.3
- 3.0.2
- 3.0.1
- 3.0.0



# Usage

There is 2 primary ways of buliding and running this container


## docker build

To build your own image run:

    docker build -t <username>/redis-cluster .

    # or

    make build

And to run the container use:

    docker run -i -t -p 7000:7000 -p 7001:7001 -p 7002:7002 -p 7003:7003 -p 7004:7004 -p 7005:7005 -p 7006:7006 -p 7007:7007

    # or

    make run

    # and top stop the container run

    make stop

To connect to your cluster you can use the redis-cli tool:

    redis-cli -c -p 7000


## docker compose

It is also possible to build the container using docker-compose. The advantage with a compose build is that it simplifies container management.

To build the container run:

    docker-compose -f docker-compose.yml build

    # or

    make compose-build

To start the container run:

    docker-compose -f docker-compose.yml up

    # or

    make compose-up

    # and to stpo the container run

    make compose-stop

To connection to your cluster you can run redis-cli tool:

    redis-cli -c -p 7000


## Build alternative redis versions

For a release to be buildable it needs to be present at this url: http://download.redis.io/releases/


### docker build

To set a different redis version use the argument --build-arg

    # Example
    docker build --build-arg redis_version=3.2.0 -t grokzen/redis-cluster .


### docker-compose

To set a different redis version you must change the variable 'redis_version' inside the docker-compose file.

Then you simply rebuild the compose file and it should be updated with the desired redis version.


# License

This repo is using the MIT LICENSE.

You can find it in the file [LICENSE](LICENSE)
