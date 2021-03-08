#!/usr/bin/env python
import os
import json
import sys
tcp_port=os.popen("""netstat -natp|grep -v ':::'|awk -F: '/mysqld/&&/LISTEN/{print $2}'|awk '{print $1}' """)
port_slave = []
port_result = []
for port in tcp_port.readlines():
    r = os.path.basename(port.strip())
    status=os.system("""/usr/bin/mysql -h127.0.0.1 -uzabbix -pzabbix -P %s -e "show slave status\G" | egrep -q 'Slave_IO_Running|Slave_SQL_Running:' """ % (r))
    if status == 0:
        port_slave.append(r)
if len(port_slave) == 0:
    sys.exit(0)
for p in port_slave:
    port_result += [{'{#MYSQLSLAVEPORT}':p}]
print json.dumps({'data':port_result},sort_keys=True,indent=4,separators=(',',':'))
