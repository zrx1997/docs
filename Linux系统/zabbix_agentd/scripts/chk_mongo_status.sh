#!/bin/bash
KEY="$1"
PORT="$2"
HOSTNAME="127.0.0.1"
if [ "$KEY" == "insert" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $1}' | sed 's/*//g'
elif [ "$KEY" == "query" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $2}' | sed 's/*//g'
elif [ "$KEY" == "update" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $3}' | sed 's/*//g'
elif [ "$KEY" == "delete" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $4}' | sed 's/*//g'
elif [ "$KEY" == "flushes" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $7}'
elif [ "$KEY" == "faults" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $11}'
elif [ "$KEY" == "idx_miss" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $13}'
elif [ "$KEY" == "qr" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $14}' | awk -F"|" '{print $1}'
elif [ "$KEY" == "qw" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $14}' | awk -F"|" '{print $2}'
elif [ "$KEY" == "ar" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $15}' | awk -F"|" '{print $1}'
elif [ "$KEY" == "aw" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $15}' | awk -F"|" '{print $2}'
elif [ "$KEY" == "conn" ]; then
    /usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --quiet --noheaders --rowcount 1 1 | awk '{print $18}'
elif [ "$KEY" == "repl" ]; then
    role=`/usr/local/bin/mongostat -u zabbix -p zabbix --port $PORT --authenticationDatabase admin --quiet --noheaders --rowcount 1 1 | awk '{print $18}'`
    if [[ "$role" == "PRI" ]] || [[ "$role" == "SEC" ]];then
        echo 1
    else
        echo 0
    fi
else
    exit 2
fi
