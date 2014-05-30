FROM ubuntu:12.04
MAINTAINER Johan Grokzen Andersson <Grokzen@gmail.com>

# Upgrade the base image with latests packages
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y

# Install system dependencies
RUN apt-get install -y gcc make g++ build-essential libc6-dev tcl git supervisor

# checkout the 3.0 (Cluster support) branch from official repo
RUN git clone -b 3.0 https://github.com/antirez/redis.git

# Build redis from source
RUN (cd /redis && make)

# Install ruby dependencies so we can bootstrap the cluster via redis-trib.rb
RUN apt-get -y install ruby rubygems
RUN gem install redis

# Because Git cannot track empty folders we have to create them manually...
RUN mkdir /redis-data && mkdir /redis-data/7000 && mkdir /redis-data/7001 && mkdir /redis-data/7002 && mkdir /redis-data/7003 && mkdir /redis-data/7004 && mkdir /redis-data/7005

# Add all config files for all clusters
ADD ./docker-data/redis-conf /redis-conf

# Add supervisord configuration
ADD ./docker-data/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose all cluster ports to the outside
EXPOSE 7000
EXPOSE 7001
EXPOSE 7002
EXPOSE 7003
EXPOSE 7004
EXPOSE 7005

# Add startup script
ADD ./docker-data/start.sh /start.sh
RUN chmod 755 /start.sh

# ENTRYPOINT ["/bin/bash"]
CMD ["/bin/bash",  "/start.sh"]
