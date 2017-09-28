FROM redis:4-alpine

MAINTAINER Hugo LE GLEUT <legleuthugo@gmail.com>

# Install system dependencies
RUN apk update && \
    apk add apkbuild-gem-resolver supervisor gettext && \
    rm -rf /var/cache

RUN gem install --no-document redis

RUN mkdir /redis-conf
RUN mkdir /redis-data
RUN mkdir /var/log/supervisor

COPY ./docker-data/redis-cluster.tmpl /redis-conf/redis-cluster.tmpl

# Add supervisord configuration
COPY ./docker-data/supervisord.conf /redis-conf/supervisord.conf

# Add supervisord configuration
COPY ./docker-data/redis-trib.rb /redis-trib.rb
RUN chmod 755 /redis-trib.rb

# Add startup script
COPY ./docker-data/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh

EXPOSE 7000 7001 7002 7003 7004 7005 7006 7007

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["redis-cluster"]
