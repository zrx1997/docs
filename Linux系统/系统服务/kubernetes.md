

### Kubernetes高可用集群安装

#### 简介

根据k8s社区的文档及官方文档参考，可以HA拓扑分为两种模式

- Stacked etcd topology（堆叠ETCD）
- External etcd topology（外部ETCD）



**堆叠ETCD**: 每个master节点上运行一个apiserver和etcd, etcd只与本节点apiserver通信

![image-20210910091113754](https://raw.githubusercontent.com/adcwb/storages/master/image-20210910091113754.png)



**外部ETCD**: etcd集群运行在单独的主机上，每个etcd都与apiserver节点通信。

![image-20210910091206495](https://raw.githubusercontent.com/adcwb/storages/master/image-20210910091206495.png)

#### 环境准备

![image-20210910095100308](https://raw.githubusercontent.com/adcwb/storages/master/image-20210910095100308.png)

1. 由外部负载均衡器提供一个vip，流量负载到keepalived master节点上。
2. 当keepalived节点出现故障, vip自动漂到其他可用节点。
3. haproxy负责将流量负载到apiserver节点。
4. 三个apiserver会同时工作。注意k8s中controller-manager和scheduler只会有一个工作，其余处于backup状态。我猜测apiserver主要是读写数据库，数据一致性的问题由数据库保证，此外apiserver是k8s中最繁忙的组件，多个同时工作也有利于减轻压力。而controller-manager和scheduler主要处理执行逻辑，多个大脑同时运作可能会引发混乱。



|  主机名   |     IP地址     |    角色    |     配置      |
| :-------: | :------------: | :--------: | :-----------: |
|  master1  | 192.168.10.241 | master节点 |   4H4G 50G    |
|  master2  | 192.168.10.242 | master节点 |   4H4G 50G    |
|  master3  | 192.168.10.243 | master节点 |   4H4G 50G    |
|   node1   | 192.168.10.244 | worker节点 |   8H8G 50G    |
|   node2   | 192.168.10.245 | worker节点 |   8H8G 50G    |
|   node3   | 192.168.10.246 | worker节点 |   8H8G 50G    |
| master-lb | 192.168.10.240 |    VIP     | VIP不占用机器 |



版本信息

|     信息      |                 备注                  |
| :-----------: | :-----------------------------------: |
|   系统版本    | CentOS Linux release 7.9.2009 (Core)  |
|  docker版本   | Docker version 20.10.8, build 3967b7d |
|    k8s版本    |                1.21.x                 |
|    pod网段    |            172.168.0.0/16             |
| serverice网段 |             10.96.0.0/16              |



**声明：**在以下配置中，默认已经关闭防火墙和selinux等安全策略，若没有关闭，请参考以下命令

```bash
# 查看防火墙
systemctl status firewalld

# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

# 查看selinux
getenforce 

# 关闭selinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
```



#### 基本配置

```bash
# 以下配置信息在所有节点通用，因此只列出一台机器的

# 修改主机名
hostnamectl set-hostname master1

# 配置hosts解析
cat > /etc/hosts <<EOF
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.10.240  master-lb
192.168.10.241  master1
192.168.10.242  master2
192.168.10.243  master3
192.168.10.244  node1
192.168.10.245  node2
192.168.10.246  node3
EOF

# ssh互信
ssh-keygen -t rsa		# 生成证书文件
ssh-copy-id master1		# 将证书文件拷贝到所有的机器
ssh-copy-id master2
ssh-copy-id master3
ssh-copy-id node1
ssh-copy-id node2
ssh-copy-id node3

# 必备工具安装
yum install -y wget jq psmisc vim net-tools telnet device-mapper-persistent-data  git curl unzip lrzsz bash* 


# 关闭swap分区
swapoff -a && sysctl -w vm.swappiness=0
sed -ri '/^[^#]*swap/s@^@#@' /etc/fstab


```



##### Docker安装

```bash
# 配置epel源
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

# 安装必要的一些系统工具
yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加阿里云的docker源信息
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo

# 更新并安装Docker-CE
yum makecache fast
yum -y install docker-ce

# 配置镜像加速器

mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": ["https://gziwmbaz.mirror.aliyuncs.com"]
}
EOF

# 启动docker并设置开机启动
systemctl daemon-reload
systemctl restart docker
systemctl enable docker

# 注意：
# 官方软件源默认启用了最新的软件，您可以通过编辑软件源的方式获取各个版本的软件包。例如官方并没有将测试版本的软件源置为可用，您可以通过以下方式开启。同理可以开启各种测试版本等。
# vim /etc/yum.repos.d/docker-ce.repo
#   将[docker-ce-test]下方的enabled=0修改为enabled=1
#
# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2: 安装指定版本的Docker-CE: (VERSION例如上面的17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]
```



##### Kubernetes源

```bash

# 配置阿里云的k8s源
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

# 安装kubeadm工具
yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet

```



##### NTP服务器搭建

```bash
# 安装ntp服务
yum -y install ntp

# 编辑文件 "/etc/ntp.conf"，根据情况修改文件内容为：

driftfile  /var/lib/ntp/drift
pidfile   /var/run/ntpd.pid
logfile /var/log/ntp.log
restrict    default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery
restrict 127.0.0.1
server 127.127.1.0
fudge  127.127.1.0 stratum 10
server ntp.aliyun.com iburst minpoll 4 maxpoll 10
restrict ntp.aliyun.com nomodify notrap nopeer noquery

systemctl start ntpd
systemctl enable ntpd

ntpdate 192.168.10.241


# 其他节点时间同步
# 将集群中的某台机器配置为NTP服务器，具体配置信息请参考下面的配置NTP服务器的搭建，并配置定时任务同步时间
yum -y install ntpdate

# 手动验证
[root@master2 ~]# ntpdate master1
10 Sep 09:31:21 ntpdate[794]: adjust time server 192.168.10.241 offset 0.003334 sec

# 配置计划任务
[root@master2 ~]# crontab -e
*/1 * * * * ntpdate master1 > /dev/null 2>&1
```



#### 内核配置

```bash
# 所有节点安装ipvsadm
yum install ipvsadm ipset sysstat conntrack libseccomp -y

# 开启一些k8s集群中必须的内核参数，所有节点配置k8s内核
[root@master01 ~]# cat > /etc/sysctl.d/k8s.conf <<EOF
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
fs.may_detach_mounts = 1
vm.overcommit_memory=1
vm.panic_on_oom=0
fs.inotify.max_user_watches=89100
fs.file-max=52706963
fs.nr_open=52706963
net.netfilter.nf_conntrack_max=2310720
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl =15
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_max_orphans = 327680
net.ipv4.tcp_orphan_retries = 3
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.ip_conntrack_max = 65536
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_timestamps = 0
net.core.somaxconn = 16384
EOF

# 应用上面的配置

sysctl --system

# k8s网络使用flannel，需要设置内核参数 bridge-nf-call-iptables=1，修改这个参数需要系统有br_netfilter模块。

```



#### 高可用组件安装

##### [HAProxy](https://github.com/haproxy/haproxy)

```bash
# 所有master节点安装keepalived和haproxy，做高可用
yum install keepalived haproxy -y

# 所有Master节点配置HAProxy（详细配置参考HAProxy文档，所有Master节点的HAProxy配置相同）：

vim /etc/haproxy/haproxy.cfg

global
  maxconn  2000
  ulimit-n  16384
  log  127.0.0.1 local0 err
  stats timeout 30s

defaults
  log global
  mode  http
  option  httplog
  timeout connect 5000
  timeout client  50000
  timeout server  50000
  timeout http-request 15s
  timeout http-keep-alive 15s

frontend monitor-in
  bind *:33305
  mode http
  option httplog
  monitor-uri /monitor
 
frontend k8s-master
  bind 0.0.0.0:16443
  bind 127.0.0.1:16443
  mode tcp
  option tcplog
  tcp-request inspect-delay 5s
  default_backend k8s-master

backend k8s-master
  mode tcp
  option tcplog
  option tcp-check
  balance roundrobin
  default-server inter 10s downinter 5s rise 2 fall 2 slowstart 60s maxconn 250 maxqueue 256 weight 100
  server master1 192.168.10.41:6443  check
  server master2 192.168.10.42:6443  check
  server master3 192.168.10.43:6443  check
  
```

##### Keepalived配置

```bash
! Configuration File for keepalived

global_defs {
    router_id LVS_DEVEL
    script_user root
    enable_script_security
}

vrrp_script chk_apiserver {
    script "/etc/keepalived/check_apiserver.sh"
    interval 5
    weight -5
    fall 2  
    rise 1
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    mcast_src_ip 192.168.10.241
    virtual_router_id 51
    priority 101
    advert_int 2
    authentication {
        auth_type PASS
        auth_pass K8SHA_KA_AUTH
    }
    virtual_ipaddress {
        192.168.196.2
    }
#    track_script {
#       chk_apiserver
#    }
}
```



`/etc/keepalived/check_apiserver.sh`

```BASH
#!/bin/bash
err=0
for k in $(seq 1 3)
do
    check_code=$(pgrep haproxy)
    if [[ $check_code == "" ]]; then
        err=$(expr $err + 1)
        sleep 1
        continue
    else
        err=0
        break
    fi
done

 

if [[ $err != "0" ]]; then
    echo "systemctl stop keepalived"
    /usr/bin/systemctl stop keepalived
    exit 1
else
    exit 0
fi
```



```bash
systemctl start haproxy.service
systemctl enable haproxy.service
systemctl status haproxy.service

systemctl start keepalived.service
systemctl enable keepalived.service
systemctl status keepalived.service

```



































