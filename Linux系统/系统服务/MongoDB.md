### CentOS安装MongoDB数据库

1、下载安装包

```bash
wget http://downloads.mongodb.org/linux/mongodb-linux-x86_64-rhel70-5.0.2.tgz
```

2、解压，并将安装包放到合适的位置，如`/usr/local/mongodb`, 并添加环境变量

```bash
tar zxvf mongodb-linux-x86_64-rhel70-5.0.2.tgz
mv mongodb-linux-x86_64-rhel70-5.0.2 /usr/local/mongodb

echo "export PATH=/usr/local/mongodb/bin:\$PATH" >>/etc/profile
source /etc/profile
```

3、创建MongoDB配置文件及服务启动文件

```bash
# 创建配置文件目录
mkdir /etc/mongodb

# 配置文件，指定的日志文件，必须事先存在
[root@www ~]# cat /etc/mongodb/mongodb.conf 
bind_ip=0.0.0.0
port=27017
dbpath=/data/mongodb/data/
logpath=/data/mongodb/logs/mongodb.log
logappend=true
fork=true
maxConns=5000


# 创建数据文件存放目录
mkdir /data/mongodb/{data,logs} -p
touch /data/mongodb/logs/mongodb.log

# 创建服务启动文件
touch /usr/lib/systemd/system/mongodb.service

# 服务启动文件详情
[root@www ~]# cat /usr/lib/systemd/system/mongodb.service
[Unit]
Description=mongodb
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
ExecStart=/usr/local/mongodb/bin/mongod -f /etc/mongodb/mongodb.conf
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/usr/local/mongodb/bin/mongod --shutdown -f /etc/mongodb/mongodb.conf
PrivateTmp=true

[Install]
WantedBy=multi-user.target


# 启动MongoDB
systemctl start mongodb
systemctl status mongodb

```

4、防火墙放行

```bash
firewall-cmd --add-port=27017/tcp --permanent 
firewall-cmd --reload
```



### MongoDB复制集

![image-20210903092250414](https://raw.githubusercontent.com/adcwb/storages/master/image-20210903092250414.png)

**一、复制集概述：**

**组成：**

 	Mongodb复制集（副本集replica set）由一组Mongod实例（进程）组成，包含一个Primary节点和多个Secondary节点，Mongodb Driver（客户端）的所有数据都写入Primary，Secondary通过oplog来同步Primary的数据，保证主节点和从节点数据的一致性，复制集在完成主从复制的基础上，通过心跳机制，一旦primary节点出现宕机，则触发选举一个新的主节点，剩下的secondary节点指向新的primary，时间应该在10-30s内完成感知primary节点故障，实现高可用数据库集群；

**特点：**

 	主是唯一的，但不是固定的；
 	
 	通过oplog同步数据保证数据的一致性；
 	
 	从库无法写入（默认情况下，不使用驱动连接时，读也是不能查询的）；
 	
 	相对于传统的主从结构，复制集可以自动容灾；



**二、复制集原理：**

**角色（按是否存储数据划分）：**

 	Primary：主节点，由选举产生，负责客户端的写操作，产生oplog日志文件；
 	
 	Secondary：从节点，负责客户端的读操作，提供数据的备份和故障的切换；
 	
 	Arbiter：仲裁节点，只参与选举的投票，不会成为primary，也不向Primary同步数据，若部署了一个2个节点的复制集，1个Primary，1个Secondary，任意节点宕机，复制集将不能提供服务了（无法选出Primary），这时可以给复制集添加一个Arbiter节点，即使有节点宕机，仍能选出Primary；



**角色（按类型区分）：**

 	Standard（标准）：这种是常规节点，它存储一份完整的数据副本，参与投票选举，有可能成为主节点；
 	
 	Passive（被动）：存储完整的数据副本，参与投票，不能成为活跃节点。
 	
 	Arbiter（投票）：仲裁节点只参与投票，不接收复制的数据，也不能成为活跃节点。

​	注：每个参与节点（非仲裁者）有个优先权（0-1000），优先权（priority）为0则是被动的，不能成为活跃节点，优先权不为0的，按照由大到小选出活跃节点，优先值一样的则看谁的数据比较新；

​	注：Mongodb 3.0里，复制集成员最多50个，参与Primary选举投票的成员最多7个；

 

**选举：**

 	每个节点通过优先级定义出节点的类型（标准、被动、投票）；
 	
 	标准节点通过对比自身数据进行选举出primary节点或者secondary节点；



**影响选举的因素**：

 	1.心跳检测：复制集内成员每隔两秒向其他成员发送心跳检测信息，若10秒内无响应，则标记其为不可用；
 	
 	2.连接：在多个节点中，最少保证两个节点为活跃状态，如果集群中共三个节点，挂掉两个节点，那么剩余的节点无论状态是primary还是处于选举过程中，都会直接被降权为secondary；



**触发选举的情况**：

 	1.初始化状态 

​	 2.从节点们无法与主节点进行通信  

​	 3.主节点辞职



主节点辞职的情况：

 	1.在接收到replSetStepDown命令后；
 	
 	2.在现有的环境中，其他secondary节点的数据落后于本身10s内，且拥有更高优先级；
 	
 	3.当主节点无法与群集中多数节点通信；

​	注：当主节点辞职后，主节点将关闭自身所有的连接，避免出现客户端在从节点进行写入操作；

​                               

 **异常处理：** 

 		当Primary宕机时，如果有数据未同步到Secondary，当Primary重新加入时，如果新的Primary上已经发生了写操作，则旧Primary需要回滚部分操作，以保证数据集与新的Primary一致。旧Primary将回滚的数据写到单独的rollback目录下，数据库管理员可根据需要使用mongorestore进行恢复。



```bash
# 默认三台MongoDB数据库单机版配置完成
# MongoDB启动复制集，需要先在配置文件中声明集群的名字，每个节点都需要
replSet=mongodb_cluster

# 声明配置文件
> cfg = {
    "_id": "mongodb_cluster",
    "members": [
        {
            "_id": 0,
            "host": "43.249.28.50:27017"
        },
        {
            "_id": 1,
            "host": "106.13.208.193:27017"
        },
        {
            "_id": 2,
            "host": "208.90.122.143:27017"
        }
    ]
}

# 初始化集群
> rs.initiate(cfg)
{ "ok" : 1 }

rs.add()			# 添加标准节点
rs.remove()			# 删除标准节点
rs.isMaster()		# 查看复制集节点
rs.initiate(cfg)	# 初始化节点
rs.addArb("ip:port")	# 添加仲裁节点，有就添加
rs.printSlaveReplicationInfo()			# 查看节点信息
rs.printReplicationInfo()
db.oplog.rs.stats()	

注意：
	secondary节点默认无法读取，可以通过以下方式或者驱动方式实现
		> db.getMongo().setSecondaryOk();
在初始化集群的时候，还可以手动指定集群的优先级
	cfg={"_id":"haha","members":[{"_id":0,"host":"43.249.28.50:27017","priority":100},{"_id":1,"host":"106.13.208.193:27017","priority":100},{"_id":2,"host":"208.90.122.143:27017","priority":10}]}
	
```

查看集群状态

```bash
mongodb_cluster:SECONDARY>  rs.status()
{
	"set" : "mongodb_cluster",
	"date" : ISODate("2021-09-02T15:01:21.612Z"),
	"myState" : 2,
	"term" : NumberLong(0),
	"syncSourceHost" : "",
	"syncSourceId" : -1,
	"heartbeatIntervalMillis" : NumberLong(2000),
	"majorityVoteCount" : 2,
	"writeMajorityCount" : 2,
	"votingMembersCount" : 3,
	"writableVotingMembersCount" : 3,
	"optimes" : {
		"lastCommittedOpTime" : {
			"ts" : Timestamp(0, 0),
			"t" : NumberLong(-1)
		},
		"lastCommittedWallTime" : ISODate("1970-01-01T00:00:00Z"),
		"appliedOpTime" : {
			"ts" : Timestamp(1630594860, 1),
			"t" : NumberLong(-1)
		},
		"durableOpTime" : {
			"ts" : Timestamp(1630594860, 1),
			"t" : NumberLong(-1)
		},
		"lastAppliedWallTime" : ISODate("2021-09-02T15:01:00.867Z"),
		"lastDurableWallTime" : ISODate("2021-09-02T15:01:00.867Z")
	},
	"lastStableRecoveryTimestamp" : Timestamp(0, 0),
	"members" : [
		{
			"_id" : 0,
			"name" : "43.249.28.50:27017",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 952,
			"optime" : {
				"ts" : Timestamp(1630594860, 1),
				"t" : NumberLong(-1)
			},
			"optimeDate" : ISODate("2021-09-02T15:01:00Z"),
			"syncSourceHost" : "",
			"syncSourceId" : -1,
			"infoMessage" : "",
			"configVersion" : 1,
			"configTerm" : 0,
			"self" : true,
			"lastHeartbeatMessage" : ""
		},
		{
			"_id" : 1,
			"name" : "106.13.208.193:27017",
			"health" : 1,
			"state" : 0,
			"stateStr" : "STARTUP",
			"uptime" : 20,
			"optime" : {
				"ts" : Timestamp(0, 0),
				"t" : NumberLong(-1)
			},
			"optimeDurable" : {
				"ts" : Timestamp(0, 0),
				"t" : NumberLong(-1)
			},
			"optimeDate" : ISODate("1970-01-01T00:00:00Z"),
			"optimeDurableDate" : ISODate("1970-01-01T00:00:00Z"),
			"lastHeartbeat" : ISODate("2021-09-02T15:01:21.122Z"),
			"lastHeartbeatRecv" : ISODate("1970-01-01T00:00:00Z"),
			"pingMs" : NumberLong(83),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "",
			"syncSourceId" : -1,
			"infoMessage" : "",
			"configVersion" : -2,
			"configTerm" : -1
		},
		{
			"_id" : 2,
			"name" : "208.90.122.143:27017",
			"health" : 1,
			"state" : 0,
			"stateStr" : "STARTUP",
			"uptime" : 20,
			"optime" : {
				"ts" : Timestamp(0, 0),
				"t" : NumberLong(-1)
			},
			"optimeDurable" : {
				"ts" : Timestamp(0, 0),
				"t" : NumberLong(-1)
			},
			"optimeDate" : ISODate("1970-01-01T00:00:00Z"),
			"optimeDurableDate" : ISODate("1970-01-01T00:00:00Z"),
			"lastHeartbeat" : ISODate("2021-09-02T15:01:21.212Z"),
			"lastHeartbeatRecv" : ISODate("1970-01-01T00:00:00Z"),
			"pingMs" : NumberLong(184),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "",
			"syncSourceId" : -1,
			"infoMessage" : "",
			"configVersion" : -2,
			"configTerm" : -1
		}
	],
	"ok" : 1,
	"$clusterTime" : {
		"clusterTime" : Timestamp(1630594860, 1),
		"signature" : {
			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
			"keyId" : NumberLong(0)
		}
	},
	"operationTime" : Timestamp(1630594860, 1)
}

```



查看复制集节点

```bash
mongodb_cluster:PRIMARY> rs.isMaster()
{
	"topologyVersion" : {
		"processId" : ObjectId("6130e389412eb5232ea1228d"),
		"counter" : NumberLong(6)
	},
	"hosts" : [
		"43.249.28.50:27017",
		"106.13.208.193:27017",
		"208.90.122.143:27017"
	],
	"setName" : "mongodb_cluster",
	"setVersion" : 1,
	"ismaster" : true,
	"secondary" : false,
	"primary" : "43.249.28.50:27017",
	"me" : "43.249.28.50:27017",
	"electionId" : ObjectId("7fffffff0000000000000001"),
	"lastWrite" : {
		"opTime" : {
			"ts" : Timestamp(1630631577, 1),
			"t" : NumberLong(1)
		},
		"lastWriteDate" : ISODate("2021-09-03T01:12:57Z"),
		"majorityOpTime" : {
			"ts" : Timestamp(1630631577, 1),
			"t" : NumberLong(1)
		},
		"majorityWriteDate" : ISODate("2021-09-03T01:12:57Z")
	},
	"maxBsonObjectSize" : 16777216,
	"maxMessageSizeBytes" : 48000000,
	"maxWriteBatchSize" : 100000,
	"localTime" : ISODate("2021-09-03T01:13:03.971Z"),
	"logicalSessionTimeoutMinutes" : 30,
	"connectionId" : 1,
	"minWireVersion" : 0,
	"maxWireVersion" : 13,
	"readOnly" : false,
	"ok" : 1,
	"$clusterTime" : {
		"clusterTime" : Timestamp(1630631577, 1),
		"signature" : {
			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
			"keyId" : NumberLong(0)
		}
	},
	"operationTime" : Timestamp(1630631577, 1)
}
mongodb_cluster:PRIMARY> 

```

### 部署用户认证登录（密钥对）

```bash
mongodb_cluster:PRIMARY> use admin
switched to db admin
mongodb_cluster:PRIMARY> db.createUser({"user":"root","pwd":"HyvBV2mb%8tf1kLx8DT%0TG7uEaKSuvbsD*9R0dXox1cXsqDH%1#Cd#%#Npjvp6Y","roles":["root"]})
Successfully added user: { "user" : "root", "roles" : [ "root" ] }


# 认证
use admin
db.auth("root", "HyvBV2mb%8tf1kLx8DT%0TG7uEaKSuvbsD*9R0dXox1cXsqDH%1#Cd#%#Npjvp6Y")

```



### MongoDB分片

**一、分片概述：**

​	**概述：**

​			分片（sharding）是指将数据库拆分，将其分散在不同的机器上的过程。分片集群（sharded cluster）是一种水平扩展数据库系统性能的方法，能够将数据集分布式存储在不同的分片（shard）上，每个分片只保存数据集的一部分，MongoDB保证各个分片之间不会有重复的数据，所有分片保存的数据之和就是完整的数据集。分片集群将数据集分布式存储，能够将负载分摊到多个分片上，每个分片只负责读写一部分数据，充分利用了各个shard的系统资源，提高数据库系统的吞吐量。

​			注：mongodb3.2版本后，分片技术必须结合复制集完成；

​	**应用场景：**

​		1.单台机器的磁盘不够用了，使用分片解决磁盘空间的问题。

​		2.单个mongod已经不能满足写数据的性能要求。通过分片让写压力分散到各个分片上面，使用分片服务器自身的资源。

​		3.想把大量数据放到内存里提高性能。和上面一样，通过分片使用分片服务器自身的资源。

 

**二、分片存储原理：**

![image-20210903102847105](https://raw.githubusercontent.com/adcwb/storages/master/image-20210903102847105.png)



**存储方式：**

​		数据集被拆分成数据块（chunk），每个数据块包含多个doc，数据块分布式存储在分片集群中。

**角色：**

​		**Config server**：MongoDB负责追踪数据块在shard上的分布信息，每个分片存储哪些数据块，叫做分片的元数据，保存在config server上的数据库 config中，一般使用3台config server，所有config server中的config数据库必须完全相同（建议将config server部署在不同的服务器，以保证稳定性）；

​		**Shard server**：将数据进行分片，拆分成数据块（chunk），每个trunk块的大小默认为64M，数据块真正存放的单位；

​		**Mongos server**：数据库集群请求的入口，所有的请求都通过mongos进行协调，查看分片的元数据，查找chunk存放位置，mongos自己就是一个请求分发中心，在生产环境通常有多mongos作为请求的入口，防止其中一个挂掉所有的mongodb请求都没有办法操作。

 

**总结：**

​			应用请求mongos来操作mongodb的增删改查，配置服务器存储数据库元信息，并且和mongos做同步，数据最终存入在shard（分片）上，为了防止数据丢失，同步在副本集中存储了一份，仲裁节点在数据存储到分片的时候决定存储到哪个节点。



**三、分片的片键；**

​	**概述：**

​			片键是文档的一个属性字段或是一个复合索引字段，一旦建立后则不可改变，片键是拆分数据的关键的依据，如若在数据极为庞大的场景下，片键决定了数据在分片的过程中数据的存储位置，直接会影响集群的性能；

​			注：创建片键时，需要有一个支撑片键运行的索引；



**片键分类：**

​		1、递增片键：使用时间戳，日期，自增的主键，ObjectId，_id等，此类片键的写入操作集中在一个分片服务器上，写入不具有分散性，这会导致单台服务器压力较大，但分割比较容易，这台服务器可能会成为性能瓶颈；



​		2、哈希片键：也称之为散列索引，使用一个哈希索引字段作为片键，优点是使数据在各节点分布比较均匀，数据写入可随机分发到每个分片服务器上，把写入的压力分散到了各个服务器上。但是读也是随机的，可能会命中更多的分片，但是缺点是无法实现范围区分；



​		3、组合片键： 数据库中没有比较合适的键值供片键选择，或者是打算使用的片键基数太小（即变化少如星期只有7天可变化），可以选另一个字段使用组合片键，甚至可以添加冗余字段来组合；	



​		4、标签片键：数据存储在指定的分片服务器上，可以为分片添加tag标签，然后指定相应的tag，比如让10.*.*.*(T)出现在shard0000上，11.*.*.*(Q)出现在shard0001或shard0002上，就可以使用tag让均衡器指定分发；



