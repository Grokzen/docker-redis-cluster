# This tag use ubuntu 14.04
FROM phusion/baseimage:0.9.15

MAINTAINER Johan Grokzen Andersson <Grokzen@gmail.com>

ENV HOME /root

RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Some Environment Variables
ENV DEBIAN_FRONTEND noninteractive

# # Ensure UTF-8 lang and locale
RUN locale-gen en_US.UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8

# Initial update and install of dependency that can add apt-repos
RUN apt-get -y update && apt-get install -y software-properties-common python-software-properties

# Add global apt repos
RUN add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise universe" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise main restricted universe multiverse" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise-updates main restricted universe multiverse" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise-backports main restricted universe multiverse"
RUN apt-get update && apt-get -y upgrade

# Install system dependencies
RUN apt-get install -y gcc make g++ build-essential libc6-dev tcl git supervisor ruby

# Must be installed seperate from ruby or it will complain about broken package
RUN apt-get install -y rubygems

# checkout the 3.0 (Cluster support) branch from official repo
RUN git clone -b 3.0 https://github.com/antirez/redis.git

# Build redis from source
RUN (cd /redis && make)

# Install ruby dependencies so we can bootstrap the cluster via redis-trib.rb
RUN gem install redis

# Because Git cannot track empty folders we have to create them manually...
RUN mkdir /redis-data && mkdir /redis-data/7000 && mkdir /redis-data/7001 && mkdir /redis-data/7002 && mkdir /redis-data/7003 && mkdir /redis-data/7004 && mkdir /redis-data/7005 && mkdir /redis-data/7006 && mkdir /redis-data/7007

# Add all config files for all clusters
ADD ./docker-data/redis-conf /redis-conf

# Add supervisord configuration
ADD ./docker-data/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add startup script
ADD ./docker-data/start.sh /start.sh
RUN chmod 755 /start.sh

# TODO: This command is the one that should be runned but currently start.sh script crashes out with an error
# CMD ["/sbin/my_init", "--enable-insecure-key", "--", "/bin/bash -c '/start.sh'"]

CMD ["/bin/bash", "/start.sh"]
