# docker-redis-cluster

[![Docker Stars](https://img.shields.io/docker/stars/makeomatic/redis-cluster.svg)](hub])
[![Docker Pulls](https://img.shields.io/docker/pulls/makeomatic/redis-cluster.svg)](hub])

Docker image with redis based on official redis-alpine The main usage for this container is to test redis cluster code.
The cluster is 3 redis instances running with 3 master & 0 slaves. They run on ports 7000 to 7002.
This image requires at least `Docker` version 1.10 but the latest version is recommended.

# Available tags

The following tags with pre-built images is available on `docker-hub`.

- latest == 3.2.9

# Usage

There is 2 primary ways of buliding and running this container

## docker build

To build your own image run:

    docker build -t <username>/redis-cluster .

    # or

    make build

And to run the container use:

    docker run -i -t -p 7000:7000 -p 7001:7001 -p 7002:7002

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

    # and to stop the container run

    make compose-stop

To connection to your cluster you can run redis-cli tool:

    redis-cli -c -p 7000
