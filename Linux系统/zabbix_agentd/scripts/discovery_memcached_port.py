#!/usr/bin/env python
import os
import json
t=os.popen("""netstat -natp|grep -v ':::'|awk -F: '/memcached/&&/LISTEN/{print $2}'|awk '{print $1}' """)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#MEMCACHEDPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
