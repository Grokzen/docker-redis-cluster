#!/bin/sh

if [ "$1" = 'redis-cluster' ]; then
    for port in `seq 7000 7002`; do
      mkdir -p /redis-conf/${port}
      mkdir -p /redis-data/${port}

      if [ -e /redis-data/${port}/nodes.conf ]; then
        rm /redis-data/${port}/nodes.conf
      fi
    done

    for port in `seq 7000 7002`; do
      PORT=${port} envsubst < /redis-conf/redis-cluster.tmpl > /redis-conf/${port}/redis.conf
    done

    supervisord -c /etc/supervisor/supervisord.conf
    sleep 3

    IP=`ifconfig | grep "inet addr:17" | cut -f2 -d ":" | cut -f1 -d " "`
    echo "yes" | ruby /redis-trib.rb create --replicas 0 ${IP}:7000 ${IP}:7001 ${IP}:7002
    tail -f /var/log/redis*.log
else
  exec "$@"
fi
