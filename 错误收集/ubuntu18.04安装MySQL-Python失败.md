错误：

```bash
(mj) moluo@ubuntu:~/Desktop/Codes$ pip install MySQL-python
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More details about Python 2 support in pip can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support pip 21.0 will remove support for this functionality.
Collecting MySQL-python
  Using cached MySQL-python-1.2.5.zip (108 kB)
Building wheels for collected packages: MySQL-python
  Building wheel for MySQL-python (setup.py) ... error
  ERROR: Command errored out with exit status 1:
   command: /home/moluo/.virtualenvs/mj/bin/python2 -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"'; __file__='"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-gqu1U_
       cwd: /tmp/pip-install-b89oA0/mysql-python/
  Complete output (30 lines):
  running bdist_wheel
  running build
  running build_py
  creating build
  creating build/lib.linux-x86_64-2.7
  copying _mysql_exceptions.py -> build/lib.linux-x86_64-2.7
  creating build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/converters.py -> build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/connections.py -> build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/cursors.py -> build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/release.py -> build/lib.linux-x86_64-2.7/MySQLdb
  copying MySQLdb/times.py -> build/lib.linux-x86_64-2.7/MySQLdb
  creating build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/CR.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/FIELD_TYPE.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/ER.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/FLAG.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/REFRESH.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  copying MySQLdb/constants/CLIENT.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
  running build_ext
  building '_mysql' extension
  creating build/temp.linux-x86_64-2.7
  x86_64-linux-gnu-gcc -pthread -fno-strict-aliasing -Wdate-time -D_FORTIFY_SOURCE=2 -g -fdebug-prefix-map=/build/python2.7-rrBAp6/python2.7-2.7.17=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Dversion_info=(1,2,5,'final',1) -D__version__=1.2.5 -I/usr/include/mysql -I/usr/include/python2.7 -c _mysql.c -o build/temp.linux-x86_64-2.7/_mysql.o
  _mysql.c:29:10: fatal error: Python.h: 没有那个文件或目录
   #include "Python.h"
            ^~~~~~~~~~
  compilation terminated.
  error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
  ----------------------------------------
  ERROR: Failed building wheel for MySQL-python
  Running setup.py clean for MySQL-python
Failed to build MySQL-python
Installing collected packages: MySQL-python
    Running setup.py install for MySQL-python ... error
    ERROR: Command errored out with exit status 1:
     command: /home/moluo/.virtualenvs/mj/bin/python2 -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"'; __file__='"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /tmp/pip-record-_reHJH/install-record.txt --single-version-externally-managed --compile --install-headers /home/moluo/.virtualenvs/mj/include/site/python2.7/MySQL-python
         cwd: /tmp/pip-install-b89oA0/mysql-python/
    Complete output (30 lines):
    running install
    running build
    running build_py
    creating build
    creating build/lib.linux-x86_64-2.7
    copying _mysql_exceptions.py -> build/lib.linux-x86_64-2.7
    creating build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/converters.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/connections.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/cursors.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/release.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/times.py -> build/lib.linux-x86_64-2.7/MySQLdb
    creating build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/CR.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/FIELD_TYPE.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/ER.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/FLAG.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/REFRESH.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/CLIENT.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    running build_ext
    building '_mysql' extension
    creating build/temp.linux-x86_64-2.7
    x86_64-linux-gnu-gcc -pthread -fno-strict-aliasing -Wdate-time -D_FORTIFY_SOURCE=2 -g -fdebug-prefix-map=/build/python2.7-rrBAp6/python2.7-2.7.17=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Dversion_info=(1,2,5,'final',1) -D__version__=1.2.5 -I/usr/include/mysql -I/usr/include/python2.7 -c _mysql.c -o build/temp.linux-x86_64-2.7/_mysql.o
    _mysql.c:29:10: fatal error: Python.h: 没有那个文件或目录
     #include "Python.h"
              ^~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
    ----------------------------------------
ERROR: Command errored out with exit status 1: /home/moluo/.virtualenvs/mj/bin/python2 -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"'; __file__='"'"'/tmp/pip-install-b89oA0/mysql-python/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /tmp/pip-record-_reHJH/install-record.txt --single-version-externally-managed --compile --install-headers /home/moluo/.virtualenvs/mj/include/site/python2.7/MySQL-python Check the logs for full command output.
```

解决：

```bash
sudo apt install python-dev
sudo apt install libmysqld-dev[报错也没事]
sudo apt install libmysqlclient-dev
pip install MySQL-python
```

如果安装过慢，则修改当前ubuntu的源

```
sudo cp /etc/apt/sources.list  /etc/apt/sources.list.backup
sudo vim /etc/apt/sources.list
```

在sources.list文件最前面，添加如下内容：

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

保存文件并退出，接着更新源

```
:wq

sudo apt-get update
```

如果无法更新，显示错误如下：
`无法获得锁 /var/lib/apt/lists/lock - open (11: 资源暂时不可用)`

则删除文件，再更新

```
sudo rm /var/lib/apt/lists/lock
sudo apt-get update
```



若安装上面的包后还是报错，则直接将文件下载下来

```bash
sudo wget https://raw.githubusercontent.com/paulfitz/mysql-connector-c/master/include/my_config.h -O /usr/include/mysql/my_config.h
```

