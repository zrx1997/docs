#!/usr/bin/env python
import os
import json
t=os.popen("""ps -ef | grep mongod | grep -v grep | awk '{split($0,a,"port"); print a[2]}' | cut -d" " -f2""")
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#MONGOPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
