#!/usr/bin/env python
import os
import json
t=os.popen("""ls -l /dev/shm/php-fpm-2* | awk '{print $NF}' | cut -d"-" -f3 | cut -d"." -f1""")
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#PHPFPMPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))