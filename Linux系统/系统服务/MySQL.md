### CentOS7安装MySql

下载安装包(mysql 5.7+)

```bash
wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
```

运行安装包

	yum -y install mysql57-community-release-el7-10.noarch.rpm

安装数据库

	yum -y install mysql-community-server

启动服务

	systemctl start mysqld.service && systemctl enable mysqld.service
	systemctl status mysqld.service

使用默认密码进入数据库

	grep "password" /var/log/mysqld.log
	mysql -uroot -p

修改密码，注意密码复杂度要求

	ALTER USER 'root'@'localhost' IDENTIFIED BY 'V3QM$FhKuSqcP@Xk<H+U8wIC_m1T?vn>';

授权远程访问

	grant all privileges on *.* to 'root'@'%' identified by 'V3QM$FhKuSqcP@Xk<H+U8wIC_m1T?vn>' with grant option;

创建用户

```bash
create user 'slave1'@'%' identified by 'QNm*6A<.Cu$:M8Plxq%dv^B]IcW;@sig';

create user 'slave2'@'%' identified by 'QNm*6A<.Cu$:M8Plxq%dv^B]IcW;@sig';
```

刷新权限

	flush privileges;

MySQL默认源在国外，如果在国内连接的话，可能会特别慢，这个时候可以去官网下载别人打包好的tar包，解压安装即可

	wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.34-1.el7.x86_64.rpm-bundle.tar
	tar xvf mysql-5.7.34-1.el7.x86_64.rpm-bundle.tar
	yum -y install ./mysql-community-*
	systemctl start mysqld.service



### MySQL主动复制

搭建并测试一主两从的主从复制环境，提高数据库的可用性和容错性

拓扑示例

![image-20210902112612921](https://raw.githubusercontent.com/adcwb/storages/master/image-20210902112612921.png)

![image-20210902105050670](https://raw.githubusercontent.com/adcwb/storages/master/image-20210902105050670.png)

环境准备

|       系统类型        |     IP地址      |      主机名      |                         所需软件                         |          硬件          |
| :-------------------: | :-------------: | :--------------: | :------------------------------------------------------: | :--------------------: |
|    Centos 7.9.2009    |  43.249.28.50   |     server1      |            boost_1_59_0.tar.gz  mysql-5.7.35             |          2H4G          |
|    Centos 7.9.2009    | 106.13.208.193  |     server2      |            boost_1_59_0.tar.gz  mysql-5.7.35             |          2H4G          |
|    Centos 7.9.2009    | 208.90.122.143  |     server3      |            boost_1_59_0.tar.gz  mysql-5.7.35             |          4H8G          |
|    Centos 7.9.2009    | 192.168.100.104 |  am.linuxfan.cn  | jdk-6u14-linux-x64.bin  amoeba-mysql-binary-2.2.0.tar.gz | 内存：512M  CPU核心：1 |
| Centos 7.4 1708 64bit | 192.168.80.138  | lamp.linuxfan.cn |                                                          | 内存：512M  CPU核心：1 |



MySQL配置文件

```bash
[root@www ~]# vim /etc/my.cnf

[mysqld]

datadir=/data/mysql/data
socket=/data/mysql/data/mysql.sock

symbolic-links=0

log-error=/data/mysql/data/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
port=3306
server_id=193                              #服务器ID
log-bin=mysql-bin                        #二进制日志文件名
binlog_format = row                       #强烈建议，其他格式可能造成数据不一致
max_binlog_size = 100M
log-slave-updates = 1                     #是否记录从服务器同步数据动作
gtid-mode = on                            #启用gitd功能
enforce-gtid-consistency = 1              #开启强制GTID一致性
master-info-repository = TABLE            #记录IO线程读取已经读取到的master binlog位置，用于slave宕机后IO线程根据文件中的POS点重新拉取binlog日志
relay-log-info-repository = TABLE         #记录SQL线程读取Master binlog的位置，用于Slave 宕机后根据文件中记录的pos点恢复Sql线程
sync-master-info = 1                      #启用确保无信息丢失；任何一个事务提交后, 将二进制日志的文件名及事件位置记录到文件中
slave-parallel-workers = 8                #设定从服务器的复制线程数；0表示关闭多线程复制功能
binlog-checksum = CRC32                   #设置binlog校验算法（循环冗余校验码）
master-verify-checksum = 1                #设置主服务器是否校验
slave-sql-verify-checksum = 1             #设置从服务器是否校验
binlog-rows-query-log_events = 1          #用于在二进制日志记录事件相关的信息，可降低故障排除的复杂度
sync_binlog = 1                           #保证master crash safe，该参数必须设置为1
innodb_flush_log_at_trx_commit = 1        #保证master crash safe，该参数必须设置为1


```



```bash
change master to master_host='43.249.28.50',master_port=3306,master_user='slave1',master_password='QNm*6A<.Cu$:M8Plxq%dv^B]IcW;@sig',master_log_file='mysql-bin.000005',master_log_pos=66813; 

change master to master_host='43.249.28.50',master_port=3306,master_user='slave2',master_password='QNm*6A<.Cu$:M8Plxq%dv^B]IcW;@sig',master_log_file='mysql-bin.000005',master_log_pos=66813; 
```





