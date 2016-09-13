FROM redis:3.2.4

MAINTAINER Johan Andersson <Grokzen@gmail.com>

# Some Environment Variables
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -yqq \
      net-tools supervisor ruby rubygems locales gettext-base && \
    apt-get clean -yqq

# # Ensure UTF-8 lang and locale
RUN locale-gen en_US.UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8

RUN gem install redis

RUN wget -qO redis.tar.gz $REDIS_DOWNLOAD_URL \
    && echo "$REDIS_DOWNLOAD_SHA1 *redis.tar.gz" | sha1sum -c - \
    && tar xfz redis.tar.gz -C / \
    && mv /redis-$REDIS_VERSION /redis

RUN mkdir /redis-conf

COPY ./docker-data/redis-cluster.tmpl /redis-cluster.tmpl
COPY ./docker-data/redis.tmpl /redis.tmpl

# Add supervisord configuration
COPY ./docker-data/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add startup script
COPY ./docker-data/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh

EXPOSE 7000 7001 7002 7003 7004 7005 7006 7007

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["redis-cluster"]
