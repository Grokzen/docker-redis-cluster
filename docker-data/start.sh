supervisord
sleep 3

# redis cluster doesn't play well with docker (or other NAT'd environments), have to explicitly advertise externally routable IP
IP=`ifconfig eth1 | grep "inet addr:" | cut -f2 -d ":" | cut -f1 -d " "`
echo "yes" | ruby /redis/src/redis-trib.rb create --replicas 1 ${IP}:7000 ${IP}:7001 ${IP}:7002 ${IP}:7003 ${IP}:7004 ${IP}:7005
tail -f /var/log/supervisor/redis-1.log
