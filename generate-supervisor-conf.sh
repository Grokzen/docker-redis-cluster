initial_port="$1"
max_port="$2"

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
[unix_http_server]
file=/tmp/supervisor.sock                       ; path to your socket file

[supervisord]
logfile=/supervisord.log                        ; supervisord log file
logfile_maxbytes=50MB                           ; maximum size of logfile before rotation
logfile_backups=10                              ; number of backed up logfiles
loglevel=error                                  ; info, debug, warn, trace
pidfile=/var/run/supervisord.pid                ; pidfile location
nodaemon=false                                  ; run supervisord as a daemon
minfds=1024                                     ; number of startup file descriptors
minprocs=200                                    ; number of process descriptors
user=root                                       ; default user
childlogdir=/                                   ; where child log files will live

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock         ; use a unix:// URL  for a unix socket
"

count=1
for port in `seq $initial_port $max_port`; do
  result_str="$result_str$(program_entry_template $count $port)"
  count=$((count + 1))
done

echo "$result_str"
