#!/bin/bash
METRIC="$1"
HOSTNAME=127.0.0.1
PORT="${2:-6379}"
KEY="$3"
if [ "$KEY" == "keys" ]; then
    /usr/local/bin/redis-cli -h $HOSTNAME -p $PORT info | grep "^$METRIC" | sed 's/,/:/g' | cut -d":" -f2 | cut -d"=" -f2
elif [ "$KEY" == "expires" ]; then
    /usr/local/bin/redis-cli -h $HOSTNAME -p $PORT info | grep "^$METRIC" | sed 's/,/:/g' | cut -d":" -f3 | cut -d"=" -f2
else
    /usr/local/bin/redis-cli -h $HOSTNAME -p $PORT info | grep "^$METRIC:" | awk -F':|,' '{print $2}'| sed "s/^[^0-9]//g"
fi