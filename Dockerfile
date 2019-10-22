# Build from commits based on redis:3.2
ARG redis_version=5.0.5

FROM redis@sha256:000339fb57e0ddf2d48d72f3341e47a8ca3b1beae9bdcb25a96323095b72a79b AS builder

LABEL maintainer="Johan Andersson <Grokzen@gmail.com>"

ARG redis_version

RUN apt-get update -qq \
    && apt-get install -y gcc make g++ build-essential libc6-dev tcl git supervisor ruby wget

RUN wget -qO redis.tar.gz https://github.com/antirez/redis/archive/${redis_version}.tar.gz \
    && tar xfz redis.tar.gz -C / \
    && mv /redis-$redis_version /redis

RUN (cd /redis && make)

FROM redis:${redis_version}

ARG redis_version

# Some Environment Variables
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -yqq \
      net-tools supervisor ruby rubygems locales gettext-base wget && \
    apt-get clean -yqq

# # Ensure UTF-8 lang and locale
RUN locale-gen en_US.UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8

# Necessary for gem installs due to SHA1 being weak and old cert being revoked
ENV SSL_CERT_FILE=/usr/local/etc/openssl/cert.pem

RUN gem install redis -v 4.0.2

RUN echo $redis_version > /redis-version.txt

RUN mkdir /redis-conf && \
	mkdir /redis-data

COPY --from=builder /redis /redis

COPY ./redis-cluster.tmpl /redis-conf/redis-cluster.tmpl
COPY ./redis.tmpl /redis-conf/redis.tmpl
COPY ./sentinel.tmpl /redis-conf/sentinel.tmpl

# Add startup script
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

# Add script that generates supervisor conf file based on environment variables
COPY ./generate-supervisor-conf.sh /generate-supervisor-conf.sh

RUN chmod 755 /docker-entrypoint.sh

EXPOSE 7000 7001 7002 7003 7004 7005 7006 7007 5000 5001 5002

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["redis-cluster"]
