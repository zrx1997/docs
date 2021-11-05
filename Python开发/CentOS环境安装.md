

```bash
wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz
tar zxvf Python-3.6.15.tgz 
cd Python-3.6.15/
mkdir /usr/local/python3
./configure --prefix=/usr/local/python3 --enable-optimizations
make && make instal




```





环境变量设置

```bash
# mongodb
export PATH=/usr/local/mongodb/bin:$PATH

# java
export JAVA_HOME=/usr/local/java/jdk1.8.0_311
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

# python3
export PATH=$PATH:$HOME/bin
export PATH=$PATH:/usr/local/python3/bin

# nodejs
export NODE_HOME=/usr/local/nodejs
export PATH=$NODE_HOME/bin:$PATH
export NODE_PATH=$NODE_HOME/lib/node_modules:$PATH

# golang
export GOROOT=/usr/local/golang
export GOPATH=/usr/local/golang/gocode
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

# virtualenvs
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/python3/bin/python3
source /usr/local/python3/bin/virtualenvwrapper.sh
```

