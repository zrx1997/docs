<img src="https://raw.githubusercontent.com/adcwb/storages/master/mongodb-logo.png" alt="img" style="zoom:150%;float: left;" />

# MongoDB

官方文档：https://docs.mongodb.com/

操作文档：https://www.qikegu.com/docs/3283

## 基本介绍 

MongoDB 是由C++语言编写并基于分布式文件存储的开源数据库。

MongoDB 是一款介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的NOSQL数据库。它面向文档存储，而且安装和操作起来都比较简单和容易，而且它支持各种流行编程语言进行操作，如Python，Node.js，Java，C++，PHP，C#，Ruby等。

目前在大数据、内容管理、持续交付、移动应用、社交应用、用户数据管理、数据中心等领域皆有广泛被使用。

### MongoDB相对于RDBMS的优势

-   无固定结构 。
-   数据结构由键值(key=>value)对组成。MongoDB 的文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组，单个对象的结构是清晰的。
-   没有复杂的表连接。不需要维护表与表之间的内在关联关系。
-   查询功能强大。MongoDB的查询功能几乎与SQL一样强大，使用基于文档的查询语言，可以对文档进行动态查询。
-   易于调优和扩展。具备高性能、高可用性及可伸缩性等特性
-   应用程序对象与数据库对象天然对应。
-   可以基于内存存储或者硬盘文件存储，提供丰富的查询操作和索引支持，也有事务操作，可以更快地更稳定的访问数据。

### 术语对比

|       **SQL**       |     **Mongodb**     | 描述                                      |
| :-----------------: | :-----------------: | ----------------------------------------- |
|   库（database）    |   库（database）    |                                           |
|     表（Talbe）     | 集合（Collection）  |                                           |
|   行/记录（Row）    |  文档（Document）   | Document就是json结构的一条数据记录        |
|   列/字段（Col）    | 字段/键/域（Field） |                                           |
| 主键（Primary Key） | 对象ID（ObjectId）  | _id: ObjectId("10c191e8608f19729507deea") |
|    索引（Index）    |    索引（Index）    | 也有普通索引, 唯一索引这么区分的          |

### 基本安装

目前最新版本为4.4版本，ubuntu18.04中默认安装的是3.6版本【可以继续基于这个版本进行学习，这块内容跳过即可】。

安装之前建议更新下Linux源.

```bash
# 1、备份源文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak  
# 2、添加源到sources.list中
sudo gedit /etc/apt/sources.list

# 在打开的文本中，添加阿里源
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

# 3、更新源
sudo apt-get update
```



如果要在ubuntu18.04中安装最新4.4版本mongodb，则需要完成以下命令步骤：

```bash
# 安装依赖包
sudo apt-get install libcurl4 openssl
# 关闭和卸载原有的mongodb
service mongodb stop
sudo apt-get remove mongodb

# 导入包管理系统使用的公钥
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
# 如果命令执行结果没有显示OK，则执行此命令在把上一句重新执行：sudo apt-get install gnupg

# 注册mongodb源
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# 更新源
sudo apt-get update

# 安装mongodb
sudo apt-get install -y mongodb-org=4.4.2 mongodb-org-server=4.4.2 mongodb-org-shell=4.4.2 mongodb-org-mongos=4.4.2 mongodb-org-tools=4.4.2
# 安装过程中如果提示: mongodb-org-tools : 依赖: mongodb-database-tools 但是它将不会被安装
# 终端下运行以下命令,解决:
# sudo apt-get autoremove mongodb-org-mongos mongodb-org-tools mongodb-org
# sudo apt-get install -y mongodb-org=4.4.2

# 创建数据存储目录
sudo mkdir -p /data/db

# 修改配置，开放27017端口
sudo vim /etc/mongodb.conf
# 把12行附近的port=27017左边的#号去掉
```

启动和关闭MongoDB

```bash
# 重新加载配置，并启动mongodb
sudo systemctl daemon-reload
sudo systemctl start mongod

# 查看运行状态
sudo systemctl status mongod
# 如果mongodb状态为stop，则运行 sudo systemctl enable mongod

# 停止mongodb
sudo systemctl stop mongod

# 重启mongodb
sudo systemctl restart mongod
```

进入交互终端

>   MongoDB安装完成后，默认是没有权限验证的，默认是不需要输入用户名密码即可登录的
>
>   也可以启动权限认证，但是必须注意：
>
>   mongodb默认是没有管理员账号的，所以要先切换到admin数据库添加管理员账号，再开启权限认证，否则就玩大了。

```bash
# 进入交互终端
mongo
```

效果：

```bash
MongoDB shell version v4.4.2
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("2c920d56-ddbb-4649-9191-a3bd4506a2d2") }
MongoDB server version: 4.4.2
---
The server generated these startup warnings when booting: 
		# 警告：强烈建议使用XFS文件系统，并使用WiredIger存储引擎。
		# 解释：因为当前ubuntu使用的是ext4文件系统，mongodb官方建议使用XFS文件系统功能更能发挥mongodb的性能，忽略不管
        2020-11-23T16:23:34.416+08:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
        # 警告：当前mongodb没有为数据库启用访问控制。对数据和配置的读写访问是不受限制的。
        # 解释：后面会创建数据库用户采用密码登陆的。暂时不用管
        2020-11-23T16:23:35.046+08:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
---
---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---

```

>   mongod是处理MongoDB系统的主要进程。主要负责处理数据请求，管理数据存储，和执行后台管理操作。
>
>   当我们运行mongod命令意味着正在启动MongoDB进程,并且在后台运行。
>
>    
>
>   mongo是一个命令行工具，用于连接一个特定的mongod实例。
>
>   当我们没有带参数运行mongo命令它将使用默认的端口号27017和localhost进行连接



退出交互终端

```python
exit
# quit()
```

为MongoDB创建用户

查看版本

```bash
mongo --version
# 或者终端内部使用 version()
```

## 基本操作

### 通用操作

#### 查看帮助文档

+   **help**

    ```bash
    	db.help()                    help on db methods
    	db.mycoll.help()             help on collection methods
    	sh.help()                    sharding helpers
    	rs.help()                    replica set helpers
    	help admin                   administrative help
    	help connect                 connecting to a db help
    	help keys                    key shortcuts
    	help misc                    misc things to know
    	help mr                      mapreduce
    
    	show dbs                     show database names
    	show collections             show collections in current database
    	show users                   show users in current database
    	show profile                 show most recent system.profile entries with time >= 1ms
    	show logs                    show the accessible logger names
    	show log [name]              prints out the last segment of log in memory, 'global' is default
    	use <db_name>                set current database
    	db.mycoll.find()             list objects in collection mycoll
    	db.mycoll.find( { a : 1 } )  list objects in mycoll where a == 1
    	it                           result of the last line evaluated; use to further iterate
    	DBQuery.shellBatchSize = x   set default number of items to display on shell
    	exit                         quit the mongo shell
    ```

#### 当前服务器状态

+   **db.serverStatus()**

    ```bash
    {
    	"host" : "ubuntu",    # 主机名
    	"version" : "4.4.2",  # mongodb版本
    	"process" : "mongod", # mongodb进程，主要有mongod和mongos(分片集群中)两种
    	"pid" : NumberLong(1034),  # mongod的pid进程号，可以在linux终端下使用命令 pidof mongod 验证
    	"uptime" : 105063,    # mongod服务启动的秒数
    	"uptimeMillis" : NumberLong(105063193), # mongod服务启动的毫秒数
    	"uptimeEstimate" : NumberLong(105063),  # mongod内部自己计算的启动秒数
    	"localTime" : ISODate("2020-12-08T16:01:08.230Z"), # 本地时间
    	# 连接数相关 
    	"connections" : {
    		"current" : 1,  # 当前连接数
    		"available" : 51199, # 可用连接数
    		"totalCreated" : 1,  # 截止目前为止总共创建的连接数
    		"active" : 1,   # 还在活跃的连接数
    
    	},
    
    	"globalLock" : {  # 全局锁相关信息
    		"totalTime" : NumberLong("105063115000"), # mongod启动后到现在的总时间，单位微秒
    		"currentQueue" : { # 当前等待锁队列
    			"total" : 0,   # 当前全局锁的等待个数
    			"readers" : 0, # 当前全局读锁等待个数
    			"writers" : 0  # 当前全局写锁等待个数
    		},
    		"activeClients" : {
    			"total" : 0,   # 当前活跃客户端的个数
    			"readers" : 0, # 当前活跃客户端中进行读操作的个数
    			"writers" : 0  # 当前活跃客户端中进行写操作的个数
    		}
    	},
    
    	"network" : { # 网络相关
    		"bytesIn" : NumberLong(1611),    # 数据库接收到的网络传输字节数
    		"bytesOut" : NumberLong(51269),  # 从数据库发送出去的网络传输字节数
    		"numRequests" : NumberLong(16),  # mongod接收到的总请求次数
    		
    	},
    	
    	# 操作计数器
    	"opcounters" : {
    		"insert" : NumberLong(0),  # 本次mongod实例启动至今收到的插入操作总数 
    		"query" : NumberLong(287), # 本次mongod实例启动至今收到的查询总数。
    		"update" : NumberLong(0),  # 本次mongod实例启动至今收到的更新操作总数 。
    		"delete" : NumberLong(0),  # 本次mongod实例启动至今的删除操作总数。
    		"getmore" : NumberLong(0), # 本次mongod实例启动至今“getmore”操作的总数。
    		"command" : NumberLong(588)# 本次mongod实例启动至今向数据库发出的命令总数 。
    	},
    
    	# 存储引擎,是MongoDB的核心组件,负责管理数据如何存储在硬盘（Disk）和内存（Memory）上
    	# MongoDB 支持多种不用的存储引擎（Storage Engine），MongoDB支持的存储引擎有：WiredTiger，MMAPv1和In-Memory。
    	# 1. WiredTiger，将数据持久化存储在硬盘文件中；从MongoDB 3.2 版本开始，成为MongDB默认存储引擎
    	# 2. In-Memory，将数据存储在内存中
    	# 3. MMAPv1，将数据持久化存储在硬盘文件中;
    	# WiredTiger是比MMAPv1更好用，更强大的存储引擎，WiredTiger的写操作会先写入缓存(Cache)中，并持久化到WAL(Write ahead log，写日志)，每60s或日志文件达到2GB时会做一次Checkpoint(检查点)，将当前数据进行持久化，产生一个新的快照。Wiredtiger连接初始化时，首先将数据恢复至最新的快照状态，然后根据WAL恢复数据，以保证存储可靠性。
    	# Checkpoint，检测点。将内存中的数据变更冲刷到磁盘中的数据文件中，并做一个标记点。
    	#             表示此前的数据表示已经持久存储在了数据文件中，此后的数据变更存在于内存和日志中.
    	#             是一种让数据库redo（重做）和data（数据）文件保持一致的机制。
    	#             并非Mongodb独有的，mysql中的InnoDB也有。
    
    	"storageEngine" : {
    		"name" : "wiredTiger", 
    		"supportsCommittedReads" : true,
    		"oldestRequiredTimestampForCrashRecovery" : Timestamp(0, 0),
    		"supportsPendingDrops" : true,
    		"dropPendingIdents" : NumberLong(0),
    		"supportsTwoPhaseIndexBuild" : true,
    		"supportsSnapshotReadConcern" : true,
    		"readOnly" : false,
    		"persistent" : true,
    		"backupCursorOpen" : false
    	},
    	
    
    	"transactions" : { # 事务，mongodb4.0以后新增特性，单个mongodb不支持事务，必须搭建MongoDB复制集才支持
    		"retriedCommandsCount" : NumberLong(0),
    		"retriedStatementsCount" : NumberLong(0),
    		"transactionsCollectionWriteCount" : NumberLong(0),
    		"currentActive" : NumberLong(0),
    		"currentInactive" : NumberLong(0),
    		"currentOpen" : NumberLong(0),
    		"totalAborted" : NumberLong(0),
    		"totalCommitted" : NumberLong(0),
    		"totalStarted" : NumberLong(0),
    		"totalPrepared" : NumberLong(0),
    		"totalPreparedThenCommitted" : NumberLong(0),
    		"totalPreparedThenAborted" : NumberLong(0),
    		"currentPrepared" : NumberLong(0)
    	},
    	"locks":{ # 锁相关
    	
    	},
    	"mem" : { # 内存相关
    		"bits" : 64, # 操作系统位数
    		"resident" : 18,  # 物理内存消耗,单位：M
    		"virtual" : 1566, # 虚拟内存消耗
    		"supported" : true # 是否显示额外的内存信息
    	},
    }
    ```

#### 查看当前db的连接机器地址

+   **db.getMongo()**

#### 查看日志

+   **show logs**

    

    ```bash
    show logs
    # global
    # startupWarnings
    
    # 如果要查看具体文件的日志。
    show log global
    ```



### 用户管理

#### 创建用户

**db.createUser(user, writeConcern)**

创建一个数据库新用户用db.createUser()方法，如果用户存在则返回一个用户重复错误。

错误信息：`uncaught exception: Error: couldn't add user: User "用户名@数据库" already exists`

**语法**：

```json
{
    user: "<用户名>",
    pwd: "<密码>",
	customData: { <any information> }, # 任意内容，主要是为了表示用户身份的相关介绍 
	roles: [ # 角色和权限分配
		{ role: "<role>", db: "<database>" } | "<role>",
		...
    ]
}



// 终端运行

db.createUser(
{
    "user": "root",
    "pwd": "123456",
    "customData": {"miaoshu"},
    "roles": [
        "role": "root", 
        "db": "admin"
    ]
}
)
```

>   mongo的用户是以数据库为单位来建立的，每个数据库有自己的管理员。
>
>   管理员可以管理所有数据库，但是不能直接管理其他数据库，要先在admin数据库认证后才可以。
>
>   管理员的权限设置包含了2块，分别是角色和权限，由roles属性进行设置。

##### 内置角色

```bash
数据库用户角色：read、readWrite; 
数据库管理角色：dbAdmin、dbOwner、userAdmin；
集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager； 
备份恢复角色：backup、restore； 
所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase 
超级用户角色：root
# 有几个角色间接或直接提供了系统超级用户的访问权限（dbOwner 、userAdmin、userAdminAnyDatabase）
```

##### 内置权限

```
Read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
root：只在admin数据库中可用。超级账号，超级权限
```

##### 给Admin数据库创建账户管理员

>   当前账号只能用于管理数据库账号，不能进行数据库操作。

```bash
# 进入/切换数据库到admin中
use admin
# 创建账户管理员
db.createUser({
	user: "admin",
	pwd: "123",
	roles: [
		{role: "userAdminAnyDatabase",db:"admin"}
	]
})
```

##### 创建超级管理员

>   当前账号可以进行数据库相关操作。

```bash
# 进入/切换数据库到admin中
use admin
# 创建超级管理员账号
db.createUser({
    user: "root",
    pwd: "123",
    roles: [
    	{ role: "root", db: "admin" }
    ]
})
```

##### 创建用户自己的数据库的角色

>   帐号是跟着数据库绑定的，所以是什么数据库的用户，就必须在指定库里授权和验证！！！

```bash
# 切换数据库，如果当前库不存在则自动创建
use mofang
# 创建管理员用户
db.createUser({
    user: "mofang",
    pwd: "123",
    roles: [
        { role: "dbOwner", db: "mofang"}
    ]
})
```

#### 用户信息

##### 查看当前库下的用户

>   只需要切换到对应的库中即可查看

```bash
use mofang
show users
```

##### 查看系统中所有的用户

>   需要切换到admin中使用账号管理员的权限进行操作

```bash
use admin
db.auth("root","123")
db.system.users.find()
```



#### 删除用户

>   db.system.users.remove(json条件)

```bash
# 有多种删除方式，下面是根据user用户名删除用户
db.system.users.remove({user:"mofang"})
```

#### 修改信息

##### 修改密码

>   必须切换到对应的库下
>
>   db.changeUserPassword("账户名", "新密码")

```bash
use mofang
db.changeUserPassword("mofang", "123456")
```

#### 开启mongodb账户认证机制

```bash
sudo vim /etc/mongodb.conf
# 找到22行附近的 auth=true，去掉左边注释符号(#)
auth=true
:wq
# 重启mongdb，配置生效
sudo systemctl restart mongod
```

注意：

>   如果上面重启以后，认证机制不生效，则执行如下代码：
>
>   ```bash
>   sudo pkill mongod                              # 杀死mongod服务
>   sudo mongod -f /etc/mongod.conf --fork --auth  # --auth 表示以认证模式启动服务，不加则关闭
>   ```



### 库管理

+   显示所有数据库列表【空数据库不会显示，或者说空数据库已经被删除了。】

    ```bsah
    show dbs
    ```

+   切换数据库，如果数据库不存在则创建数据库。

    ```bash
    use  <database>
    ```

+   查看当前工作的数据库

    ```json
    db
    db.getName()
    ```

+   删除当前数据库，如果数据库不存在，也会返回`{"ok":1}`

    ```json
    db.dropDatabase()
    ```

    

+   查看当前数据库状态

    ```json
    > db.stats()
    
    {
    	"db" : "mofang",
    	"collections" : 0,
    	"views" : 0,
    	"objects" : 0,
    	"avgObjSize" : 0,
    	"dataSize" : 0,
    	"storageSize" : 0,
    	"totalSize" : 0,
    	"indexes" : 0,
    	"indexSize" : 0,
    	"scaleFactor" : 1,
    	"fileSize" : 0,
    	"fsUsedSize" : 0,
    	"fsTotalSize" : 0,
    	"ok" : 1
    }
    
    ```



### 集合管理

#### 创建集合

>   在mongodb中其实不创建集合，直接添加文档，mongodb也会自动生成集合的。

```bash
# name为必填参数，options为可选参数。capped若设置值为true，则size必须也一并设置
db.createCollection(name=<集合名称>, options  = { 
	capped : <boolean>, # 创建固定集合，固定集合指限制固定数据大小的集合，当数据达到最大值会自动覆盖最早的文档内容 
	size : <bytes_size>,      # 指定固定集合存储的最大字节数，单位：字节数.
	max : <collection_size>   # 指定固定集合中包含文档的最大数量，单位：字节数
})

.
添加文档到不存在的集合中，mongodb会自动创建集合，
db.集合.insert({"name":"python入门","price" : 31.4})
```

#### 集合列表

```json
show collections 　# 或 show tables   或 db.getCollectionNames()
```

#### 删除集合

```json
db.集合.drop()
```

#### 查看集合

```json
db.getCollection("集合")
```

##### 查看集合创建信息

```json
db.printCollectionStats()
```



### 数据类型

| Type                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **ObjectID**           | 用于存储文档的ID,相当于主键                                  |
| **String**             | 字符串是最常用的数据类型，MongoDB中的字符串必须是UTF-8编码。 |
| **Integer**            | 整数类型用于存储数值。整数可以是32位，也可以是64位，这取决于你的服务器。 |
| **Double**             | 双精度类型用于存储浮点值,mongodb中没有float浮点数这个说法    |
| **Boolean**            | 布尔类型用于存储布尔值(true/ false)                          |
| **Arrays**             | 将数组、列表或多个值存储到一个键                             |
| **Timestamp**          | 时间戳，用于记录文档何时被修改或创建。                       |
| **Object**             | 用于嵌入文档,相当于子属性是另一个json而已                    |
| **Null**               | 空值,相当于 python的None                                     |
| **Symbol**             | 与字符串用法相同，常用于某些使用特殊符号的语言               |
| **Date**               | 用于以UNIX时间格式存储当前日期或时间。                       |
| **Binary data**        | 二进制数据                                                   |
| **Code**               | 用于将JavaScript代码存储到文档中                             |
| **Regular expression** | 正则表达式                                                   |



### 文档管理

#### 添加文档

>   文档的数据结构和 JSON 基本一样。所有存储在集合中的数据都是 BSON 格式。
>
>   BSON 是一种类似 JSON 的二进制形式的存储格式，是 Binary JSON 的简称。

```json
# 添加文档
# 方式1：
db.集合.insert(<document>)  # document就是一个json

# 方式2：       
db.集合.insertOne(          # 如果文档存在_id主键为更新数据，否则就添加数据。
   <document>
)

# 方式3
# 一次性添加多个文档, 多次给同一个集合建议使用insertMany比insertOne效率更好
db.集合.insertMany(
   [ <document> , <document>, ... ]
)

//  
db.mofang.insert(
    {
        "_id": "1",
        "name": "python",
        "age": "18",
        "price": 35.88
    }
)


db.mofang.insertOne(
  	{
        "_id": "1",
        "name": "python",
        "age": "18"
    }
)



db.mofang.insert(
    {
        "_id": "1",
        "name": "python",
        "age": "18",
        "price": 35.88
    },
        {
        "_id": "2",
        "name": "python",
        "age": "18",
        "price": 35.88
    },
    {
        "_id": "3",
        "name": "python",
        "age": "18",
        "price": 35.88
    }
)




```



#### 查询文档

```json
# 直接显示查询的所有
# 获取一条
db.集合.findOne(
	<query>，     # 查询条件
    {
    	<key>: 0, # 隐藏指定字段，例如："_id":0,
    	<key>: 1, # 显示指定字段，例如："title":1,
    	....
    }
)

// db.mofang.findOne({"name":"python"})
# 获取多条
db.集合.find(
	<query>,      # 查询条件
    {
    	<key>: 0, # 隐藏指定字段，例如："_id":0,
    	<key>: 1, # 显示指定字段，例如："title":1,
    	....
    }
)

//  db.mofang.find()


# 以易读的方式来格式化显示读取到的数据
db.col.find().pretty() 
```

##### 比较运算

| 操作       | 格式                                     | 范例                                  | SQL中的类似语句           |
| :--------- | :--------------------------------------- | :------------------------------------ | :------------------------ |
| 等于       | `{<key>:<val>`}<br>`{<key>:{$eq:<val>}}` | `db.集合.find({"name":"xiaoming"})`   | `where name = 'xiaoming'` |
| 小于       | `{<key>:{$lt:<val>}}`                    | `db.集合.find({"age":{$lt:17}})`      | `where age  < 17`         |
| 小于或等于 | `{<key>:{$lte:<val>}}`                   | `db.集合.find({"age":{$lte:17}})`     | `where age  <= 17`        |
| 大于       | `{<key>:{$gt:<val>}}`                    | `db.集合.find({"age":{$gt:17}})`      | `where age  > 17`         |
| 大于或等于 | `{<key>:{$gte:<val>}}`                   | `db.集合.find({"age":{$gte:17}})`     | `where age  >= 17`        |
| 不等于     | `{<key>:{$ne:<val>}}`                    | `db.集合.find({"age":{$ne:17}})`      | `where age != 17`         |
| 包含       | `{<key>:{$in:<val>}}`                    | `db.集合.find({"age":{$in:[1,2,3]}})` | `where age in (1,2,3)`    |

###### 终端运行效果

```bash
db.my_friend.find({"name":{$eq:"xiaohong"}}).pretty()
db.my_friend.find({"age":{$gt:15}}).pretty()
```



##### 逻辑运算

| 操作          | 格式                                                         | 语法                                                         |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `$and`        | `{<key>:<val>,<key>:<val>,...}`                              | db.集合.find({key1:value1, key2:value2})                     |
| `$or`         | `{$or: [{<key>: <val>}, {<key>:<val>}]}`                     | db.集合.find({$or: [{key1: value1}, {key2:value2}]})         |
| `$and`和`$or` | `{<key>:<val>, $or: [{<key>: <val>}, {<key>:<val>}]}`<br>`{$and:[{$or:[{<key>:<val>},..]},$or:[{<key>:<val>},..]}]}` | db.集合.find({key1:value1, $or: [{key1: value1}, {key2:value2}]}) |
| $not          | `{<key>:{$not:{<$运算符>:<val>}}}`                           | `$not`操作符不支持``$regex`正则表达式操作                    |



##### 其他运算符

| 操作    | 格式                                                         | 语法                                      | 说明                           |
| ------- | ------------------------------------------------------------ | ----------------------------------------- | ------------------------------ |
| $type   | `{<key>:{$type: <datetype>}}`                                | `db.集合.find({"name":{$type:'string'}})` | 匹配指定键是指定数据类型的文档 |
| $exists | `{<key>:{$exists:<bool>}`                                    | `db.集合.find({"title":{$exists:true}})`  | 匹配具有指定键的文档           |
| $regex  | `{ <key>:/模式/<修正符>}`<br>`{<key>:{$regex:/模式/<修正符>}}` | `db.集合.find({"name":{$regex:/张$/}})`   | 按正则匹配                     |

##### 排序显示

```json
db.集合.find().sort({<key>:1})  # 升序，默认为升序
db.集合.find().sort({<key>:-1}) # 倒序， 
```



##### 字段投影

`find()`方法默认将返回文档的所有数据，但是可以通过设置`find()`的第二个参数projection，设置值查询部分数据。

语法：

```json
# 获取一条
db.集合.findOne(
	<query>，     # 查询条件
    {
    	<key>: 0, # 隐藏指定字段，例如："_id":0,
    	<key>: 1, # 显示指定字段，例如："title":1,
    	....
    }
)
# 获取多条
db.集合.find(
	<query>,      # 查询条件
    {
    	<key>: 0, # 隐藏指定字段，例如："_id":0,
    	<key>: 1, # 显示指定字段，例如："title":1,
    	....
    }
)
```



#### 更新文档

```json
# 更新一条
db.集合.update(
   <query>,   # update的查询条件，一般写法：{"属性":{条件:值}}
   <update>,  # update的更新数据，一般写法 { $set:{"属性":"值"} } 或者 { $inc:{"属性":"值"} }
   {
     upsert: <boolean>, # 可选参数，如果文档不存在，是否插入objNew, true为插入，默认是false，不插入
     multi: <boolean>,  # 可选参数，是否把满足条件的所有数据全部更新
     writeConcern: <document> # 可选参数，抛出异常的级别。
   }
)

# 更新多条
db.集合.updateMany(
   <query>,   # update的查询条件，一般写法：{"属性":{条件:值}}
   <update>,  # update的对象，一般写法 { $set:{"属性":"值"} } 或者 { $inc:{"属性":"值"} }
   {
     upsert: <boolean>, # 可选参数，如果文档不存在，是否插入objNew, true为插入，默认是false，不插入
     multi: <boolean>,  # 可选参数，是否把满足条件的所有数据全部更新
     writeConcern: <document> # 可选参数，抛出异常的级别。
   }
)
```



##### update修改器

| 操作     | 语法                                                       |                                                              |
| -------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `$inc`   | `db.集合.update({<key1>:<val1>},{$inc:{<key2>:<val2>}})`   | 更新key1=val1的文档中key2的值为val2，类似python的递增递减    |
| `$set`   | `db.集合.update({<key1>:<val>}, {$set:{<key2>:<val2>}})`   | 更新key1=val1的文档中key2的值为val2，如果key2不存在则新增对应键值对 |
| `$unset` | `db.集合.update({<key1>:<val>}, {$unset:{<key2>:<val2>}})` | 移除key1=val1的文档中key2=val2这个键值对                     |
| `$push`  | `db.集合.update({<key1>:<val>}, {$push:{<key2>:<val2>}})`  | 给key1=val1的文档中key2列表增加一个数组成员val2。<br>key2必须是数组 |
| `$pull`  | `db.集合.update({<key1>:<val>}, {$pull:{<key2>:<val2>}})`  | 与push相反，给key1=val1的文档中key2列表删除指定成员val2      |
| `$pop`   | `db.集合.update({<key1>:<val>}, {$pop:{<key2>:<val2>}})`   | 给key1=val1的文档中key2列表移除第一个或最后一个成员。<br>val2只能是1(最后面)或-1(最前面)，与python相反 |



#### 删除文档

```json
db.集合.remove(
   <query>,  # remove的查询条件，一般写法：{"属性":{条件:值}}，如果不填写条件，删除所有文档
   {
     justOne: <boolean>,      # 可选删除，是否只删除查询到的第一个文档，默认为false，删除所有
     writeConcern: <document> # 可选参数，抛出异常的级别。
   }
)
```



## PyMongo

安装：

```bash
pip install pymongo
```

### 数据库连接

**数据库连接，无密码**

```python
import pymongo
mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
```

**数据库连接，有密码**

```python
# 方式1：
import pymongo
from urllib import parse
username = parse.quote_plus('mofang')   # 对用户名进行编码
password = parse.quote_plus('123456')  # 对密码进行编码
database = "mofang" # 数据库名称
host     = "127.0.0.1"
port     = "27017"
mongo = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % ( username, password, host, port, database))

"""
# 方式2：
import pymongo
from urllib import parse
username = parse.quote_plus('mofang')   # 对用户名进行编码
password = parse.quote_plus('123456')  # 对密码进行编码
database = "mofang" # 数据库名称
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017') # 组装成url进行连接
my_db = mongo["mofang"]
my_db.authenticate(username,password)
"""

"""
# 方式3：
import pymongo
from urllib import parse
username = parse.quote_plus('root')   # 对用户名进行编码
password = parse.quote_plus('123456')  # 对密码进行编码
host     = "127.0.0.1"
port     = "27017"
database = "mofang" # 数据库名称
mongo = pymongo.MongoClient('mongodb://%s:%s@%s:%s/admin' % ( username, password, host, port))
my_db = mongo[database]
my_collection = my_db["my_collection"] # 没有往集合里面保存文档之前，mongdb不会真正创建集合!
"""
```



### 数据库管理

```python
import pymongo

# 数据库连接
mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

# 创建数据库
my_db  = mongo["my_db"] # 没有往集合里面保存文档之前，mongdb不会真正创建集合!

# 查看数据库列表
print(mongo.list_database_names()) # 上面的 my_db 因为没有内容，所以没有被创建的。

# 数据库的删除,仅仅是清空所有集合就可以了
```



### 集合管理

```python
import pymongo

mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_db = mongo["my_db"]

my_collection = my_db["my_collection"] # 没有往集合里面保存文档之前，mongdb不会真正创建集合!

# 查看集合列表
print(my_db.list_collection_names())

# 删除集合
# 方式1
my_collections = my_db["notify_list"]
my_collections.drop()  # 删除成功返回true，如果集合不存在，返回false

# 方式2
my_db.drop_collection("notify_list")
```



### 文档管理

#### 添加文档

```python
from pymongo import MongoClient
connect = MongoClient("mongodb://127.0.0.1:27017")
my_db = connect["mofang"]
my_collections = my_db["my_collections"]

# 添加一条数据
document = { "name": "xiaoming", "mobile": "13012345678","age":16,"sex":True}
ret = my_collections.insert_one(document)
print(ret.inserted_id) # 返回主键ID

# 添加多条数据
data_list = [
    { "name": "xiaobai", "mobile": "13322345678","age":16,"sex":False},
    { "name": "xiaohei", "mobile": "13322345678","age":20,"sex":True},
    { "name": "xiaohong", "mobile": "13322345678","age":13,"sex":False},
    { "name": "xiaolan", "mobile": "13322345678","age":17,"sex":True},
    { "name": "xiaolv", "mobile": "13322345678","age":17,"sex":True},
    { "name": "xiaolong", "mobile": "13322345678","age":16,"sex":False},
    { "name": "xiaofei", "mobile": "13322345678","age":18,"sex":True},
]
ret = my_collections.insert_many(data_list)
print(ret.inserted_ids)
```



#### 查询文档

```python
import pymongo

mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_db = mongo["my_db"]
my_collection = my_db["my_collection"]

# 查看一个文档
ret = my_collection.find_one() # 查询不到则返回None
print(ret)

# 查看所有文档
for document in my_collection.find():  # 查询不到,返回空列表
	print(document)

# 查看文档部分字段，find和find_one的第二个参数表示控制字段的显示隐藏，1为显示，0为隐藏
for document in my_collection.find({},{ "_id": 0, "name": 1, "mobile": 1 }):
	print(document)

# 条件查询
query = { "age": 18 }
document_list = my_collection.find(query) # find_one则返回一个文档
for document in document_list:
	print(document)

# 比较运算符
query = { "age": {"$gt":17} }
document_list = my_collection.find(query)
for document in document_list:
	print(document)

# 排序显示
# 单个字段排序：
# 		sort("键", 1) 升序
# 		sort("键",-1) 降序
# 多个字段排序：
#       sort([("键1",1),("键2",-1)])
document_list = my_collection.find().sort("age")
for document in document_list:
	print(document)
    
# 限制查询结果数量
document_list = my_collections.find().limit(3)
print(document_list)
```



#### 删除文档

```python
import pymongo

mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_db = mongo["my_db"]
my_collection = my_db["my_collection"]

# 删除一个文档
query = {"name":"xiaoming"}
my_collection.delete_one(query)

# 删除多个文档
query = { "mobile": {"$regex": "^130"} }
ret = my_collection.delete_many(query)
print("删除了%d个文档" % ret.deleted_count)

# 查询一条数据出来并删除
# 返回一条数据，如果没有，则返回None
query = {"name":"xiaobai"}
document = my_collection.find_one_and_delete(query)
print(document) # {'_id': ObjectId('5fd1e9f17ee514c5ea91823c'), 'name': 'xiaobai', 'mobile': '13322345678', 'age': 16, 'sex': False}
```



#### 更新文档

```python
from pymongo import MongoClient
# 数据库链接，必须保证当前系统能正常访问mongodb！！!
connect = MongoClient("mongodb://root:123@127.0.0.1:27017/admin")
my_db = connect["mofang"]
my_collection = my_db["my_collections"]

"""更新文档"""
"""按条件更新一个文档的指定数据"""
query = { "name": "xiaofei" }
upsert = { "$set": { "age": 22 } }
ret = my_collection.update_one(query, upsert)
print(ret.modified_count) # 0 表示没有任何修改，1表示修改成功

"""按条件累加/累减指定数值一个文档的指定数据"""
query = { "name": "xiaofei" }
upsert = { "$inc": { "age": -1 } } # 累减
# upsert = { "$inc": { "age": 1 } }  # 累加
ret = my_collection.update_one(query, upsert)
print(ret.modified_count)

"""更新多条数据"""
# 把所有以"133"开头的手机码号的文档，全部改成15012345678
query = { "mobile": {"$regex":"^150"} }
upsert = { "$set": { "mobile": "18512345678" } }
ret = my_collection.update_many(query, upsert)
print(ret.modified_count)
```

