FROM debian:12-slim

LABEL maintainer="Serhii Himadieiev <gimadeevsv@gmail.com>"

# Some Environment Variables
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt update -qq && \
    apt install --no-install-recommends -yqq ruby rubygems locales wget \
    gcc make g++ build-essential libc6-dev tcl && \
    apt clean -yqq

# Ensure UTF-8 lang and locale
RUN locale-gen --purge "C.UTF-8"
ENV LANG       "C.UTF-8"
ENV LANGUAGE   "C.UTF-8"
ENV LC_ALL     "C.UTF-8"

# Necessary for gem installs due to SHA1 being weak and old cert being revoked
ENV SSL_CERT_FILE=/usr/local/etc/openssl/cert.pem

RUN gem install redis -v 5.1.0

ARG redis_version=7.2

RUN wget -qO redis.tar.gz https://github.com/redis/redis/tarball/${redis_version} \
    && tar xfz redis.tar.gz -C / \
    && mv /redis-* /redis \
    && rm redis.tar.gz

RUN (cd /redis && make)

RUN mkdir /redis-conf && mkdir /redis-data

COPY redis-cluster.tmpl /redis-conf/redis-cluster.tmpl
COPY redis.tmpl         /redis-conf/redis.tmpl
COPY sentinel.tmpl      /redis-conf/sentinel.tmpl

# Add startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Add script that generates supervisor conf file based on environment variables
COPY generate-supervisor-conf.sh /generate-supervisor-conf.sh

# Cleant up installed
RUN apt auto-remove -yqq wget gcc make g++ build-essential libc6-dev \
    && apt clean -yqq \
    && rm -rf /redis/deps /usr/lib/gcc /var/lib/apt/lists/

FROM debian:12-slim

RUN apt update -qq && \
    apt install --no-install-recommends -yqq net-tools supervisor gettext-base && \
    apt clean -yqq

COPY --from=0 /redis/src /redis/src
COPY --from=0 /redis-conf /redis-conf
COPY --from=0 /redis-data /redis-data
COPY --from=0 /docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=0 /generate-supervisor-conf.sh /generate-supervisor-conf.sh

RUN chmod 755 /docker-entrypoint.sh

EXPOSE 7000 7001 7002 7003 7004 7005 7006 7007 5000 5001 5002

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["redis-cluster"]
