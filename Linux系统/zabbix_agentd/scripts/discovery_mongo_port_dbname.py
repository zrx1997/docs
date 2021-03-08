#!/usr/bin/env python
import os
import json
p=os.popen("""ps -ef | grep mongod | grep -v grep | awk '{split($0,a,"port"); print a[2]}' | cut -d" " -f2""").readlines()
p1=p[0].strip()
t=os.popen("""/bin/echo "show dbs" | /usr/local/bin/mongo -u zabbix -p zabbix --quiet 127.0.0.1:%s/admin  | egrep -v 'admin|local' | awk '{print $1}'"""%p1)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#MONGOPORTDBNAME}':r}]

print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
