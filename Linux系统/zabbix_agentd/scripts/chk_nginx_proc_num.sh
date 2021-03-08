#!/bin/bash
proc_num=`pgrep nginx | wc -l`
nginx_config_file=`grep 'worker_processes' /usr/local/webserver/nginx/conf/nginx.conf | awk '{print $2}' | sed 's/;//g'`
if [ $proc_num -le $nginx_config_file ];
then
    echo 0
else
    echo 1
fi
