max_port="$1"

program_entry_template ()
{
  local count=$1
  local port=$2
  echo "

[program:redis-$count]
command=/redis/src/redis-server /redis-conf/$port/redis.conf
stdout_logfile=/var/log/supervisor/%(program_name)s.log
stderr_logfile=/var/log/supervisor/%(program_name)s.log
autorestart=true
"
}

result_str="
[supervisord]
nodaemon=false
"

count=1
for port in `seq 7000 $max_port`; do
  result_str="$result_str$(program_entry_template $count $port)"
  count=$((count + 1))
done

echo "$result_str"