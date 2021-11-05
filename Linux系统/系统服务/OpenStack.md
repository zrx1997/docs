## OpenStack安装

- 身份服务
- 图像服务
- 安置服务
- 计算服务
- 网络服务

我们建议您在安装最小部署服务后还安装以下组件：

- 仪表板
- 块存储服务



### 简介

```bash
版本：
	OpenStack Train版

systemctl stop firewalld

vim /etc/selinux/config
SELINUX=disabled

setenforce 0
```



### 环境准备

|   节点   |       IP地址       | 主机名  | 配置 | 备注 |
| :------: | :----------------: | :-----: | :--: | :--: |
| 控制节点 |   192.168.10.241   | master  | 4H4G |      |
| 网络节点 |   192.168.10.242   | network | 4H4G |      |
| 存储节点 |   192.168.10.243   | storage | 4H4G |      |
| 计算节点 | 192.168.10.244~246 |  node   | 8H8G |      |

`/etc/profile` 将密码声明为环境变量

```bash
export ADMIN_PASS=fc05e1929b2c057a4098
export CINDER_DBPASS=BBDERS1@bbdops.com
export CINDER_PASS=fc05e1929b2c057a4098
export DASH_DBPASS=fc05e1929b2c057a4098
export DEMO_PASS=fc05e1929b2c057a4098
export GLANCE_DBPASS=BBDERS1@bbdops.com
export GLANCE_PASS=fc05e1929b2c057a4098
export KEYSTONE_DBPASS=BBDERS1@bbdops.com
export METADATA_SECRET=fc05e1929b2c057a4098
export NEUTRON_DBPASS=BBDERS1@bbdops.com
export NEUTRON_PASS=fc05e1929b2c057a4098
export NOVA_DBPASS=BBDERS1@bbdops.com
export NOVA_PASS=fc05e1929b2c057a4098
export PLACEMENT_PASS=fc05e1929b2c057a4098
export RABBIT_PASS=fc05e1929b2c057a4098
```



**mysql安装**

```bash
# 
pass
```



安装openstack train软件源

```bash
yum install centos-release-openstack-train -y

# 客户端
yum install python-openstackclient -y

```



**消息队列**

```bash
yum install rabbitmq-server -y
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
rabbitmq-plugins enable rabbitmq_management 

# 添加用户
rabbitmqctl add_user openstack $RABBIT_PASS
# 分配权限
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
```



**安装Memcached**

```bash
yum install memcached python-memcached -y
sed -i '/OPTIONS/c\OPTIONS="-l 0.0.0.0,::1"' /etc/sysconfig/memcached
systemctl restart memcached.service
systemctl enable memcached.service
```





etcd

```bash
yum install etcd -y
cp -a /etc/etcd/etcd.conf{,.bak}

cat > /etc/etcd/etcd.conf <<EOF 
#[Member]
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="http://192.168.10.241:2380"
ETCD_LISTEN_CLIENT_URLS="http://192.168.10.241:2379"
ETCD_NAME="controller"
#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://192.168.10.241:2380"
ETCD_ADVERTISE_CLIENT_URLS="http://192.168.10.241:2379"
ETCD_INITIAL_CLUSTER="controller=http://192.168.10.241:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
ETCD_INITIAL_CLUSTER_STATE="new"
EOF

systemctl restart etcd.service
systemctl enable etcd.service 
```



keystone

**安装 keystone 认证**
https://docs.openstack.org/keystone/train/install/index-rdo.html

```bash
[root@master1 ~]# mysql -uroot -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 8
Server version: 10.3.20-MariaDB MariaDB Server

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> create database keystone;
Query OK, 1 row affected (0.001 sec)

MariaDB [(none)]> grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'KEYSTONE_DBPASS';
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> grant all privileges on keystone.* to 'keystone'@'%' identified by 'KEYSTONE_DBPASS';
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> flush privileges;
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> \q
Bye

yum install openstack-keystone httpd mod_wsgi -y
cp /etc/keystone/keystone.conf{,.bak}
egrep -v '^$|^#' /etc/keystone/keystone.conf.bak >/etc/keystone/keystone.conf



keystone-manage bootstrap --bootstrap-password $ADMIN_PASS \
  --bootstrap-admin-url http://master1:5000/v3/ \
  --bootstrap-internal-url http://master1:5000/v3/ \
  --bootstrap-public-url http://master1:5000/v3/ \
  --bootstrap-region-id RegionOne
```



```bash
# 三台机器都要做
export OS_USERNAME=admin
export OS_PASSWORD=$ADMIN_PASS
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://master1:5000/v3
```

