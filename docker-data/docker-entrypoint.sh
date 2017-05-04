#!/bin/sh

if [ "$1" = 'redis-cluster' ]; then
    for port in `seq 7001 7003`; do
      mkdir -p /redis-conf/${port}
      mkdir -p /redis-data/${port}

      if [ -e /redis-data/${port}/nodes.conf ]; then
        rm /redis-data/${port}/nodes.conf
      fi
    done

    for port in `seq 7001 7003`; do
      PORT=${port} envsubst < /redis-conf/redis-cluster.tmpl > /redis-conf/${port}/redis.conf
    done

    supervisord -c /etc/supervisor/supervisord.conf
    sleep 3

    IP=`ifconfig | grep "inet addr:17" | cut -f2 -d ":" | cut -f1 -d " "`
    echo "yes" | ruby /redis/src/redis-trib.rb create --replicas 1 ${IP}:7001 ${IP}:7002 ${IP}:7003
    tail -f /var/log/supervisor/redis*.log
else
  exec "$@"
fi
