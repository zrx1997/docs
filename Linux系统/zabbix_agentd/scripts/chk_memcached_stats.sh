#!/bin/bash
ipaddr=127.0.0.1
argv="$1"
port="$2"
/usr/local/bin/memcached-tool $ipaddr:$port stats | grep "$argv" | awk '{print $NF}'
