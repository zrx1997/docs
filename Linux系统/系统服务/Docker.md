### CentOS 7 安装docker

安装yum工具类

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
```

启动docker源

```bash
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

安装docker

```bash
yum install docker-ce
```

国内配置镜像加速器

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["https://gziwmbaz.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```



### Ubuntu 安装docker

更新ubuntu的apt源,上面如果执行过可以忽略

```bash
sudo apt-get update
```

安装包允许apt通过HTTPS使用仓库

```bash
sudo apt-get install apt-transport-https ca-certificates curl software-properties-commo
```

添加Docker官方GPG key，网络不好的话，会报错，多执行几次即可。

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

设置Docker稳定版仓库，网络不好的话，会报错，多执行几次即可。

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

添加Docker仓库后，更新apt源索引,注意，这里更新的源是关于docker的。

```bash
sudo apt-get update
```

安装最新版Docker CE（社区版）

```bash
sudo apt-get install docker-ce
```



检查Docker CE是否安装正确,hello-world是一个打印字符串的测试镜像，docker会自动下载

```bash
sudo docker run hello-world
```



### 安装脚本

```bash
#!/bin/bash


#安装网卡转发
echo '---------------------正在安装网卡转发---------------------'

cat <<EOF >  /etc/sysctl.d/docker.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward=1
EOF
sysctl -p /etc/sysctl.d/docker.conf

echo '成功！'

echo '---------------------------查看是否具备基本yum源----------------------'
#查看是否具有yum源
yum clean all && yum repolist
#安装docker yum源
echo '--------------------------即将为你安装docker yum 源---------------------'

curl -o /etc/yum.repos.d/docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
echo '成功！'

#安装指定版本的docker-ce
echo '--------------------即将为你安装docker--------------------------'

yum install -y docker-ce-18.09.9

#设置开机自启并启动docker
systemctl enable docker  
systemctl daemon-reload
systemctl start docker 
if [ $? ];then
exit
fi

#查看docker状态
echo '你的docker状态为:'
systemctl status docker
#即将为你配置docker源加速 如不需要请按 ctrl+z!
echo '================即将为你配置docker源加速 如不需要请按 ctrl+z!=================='

mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://gziwmbaz.mirror.aliyuncs.com"]    #这里可更改你的加速地址。
}
EOF
systemctl daemon-reload
systemctl restart docker
echo '安装完成！5秒后退出程序！'


# 配置文件
[root@www ~]# cat /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service containerd.service
Wants=network-online.target
Requires=docker.socket containerd.service

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always

# Note that StartLimit* options were moved from "Service" to "Unit" in systemd 229.
# Both the old, and new location are accepted by systemd 229 and up, so using the old location
# to make them work for either version of systemd.
StartLimitBurst=3

# Note that StartLimitInterval was renamed to StartLimitIntervalSec in systemd 230.
# Both the old, and new name are accepted by systemd 230 and up, so using the old name to make
# this option work for either version of systemd.
StartLimitInterval=60s

# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity

# Comment TasksMax if your systemd version does not support it.
# Only systemd 226 and above support this option.
TasksMax=infinity

# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes

# kill only the docker process, not all processes in the cgroup
KillMode=process
OOMScoreAdjust=-500

[Install]
WantedBy=multi-user.target

```





### Docker常用命令

服务启动类

```bash
systemctl start docker		# 启动
systemctl start docker		# 重启
systemctl stop docker		# 关闭
systemctl enable docker		# 开机启动
systemctl dsiable docker	# 关闭开机启动
systemctl status docker		# 查看状态
```



资源查看类

```bash
docker search			# 从Docker Hub查找镜像
docker images			# 列出所有镜像(images)
docker ps				# 列出正在运行的容器(containers)
docker ps -a			# 列出所有的容器
docker pull images		# 下载centos镜像
docker push images		# 上传镜像
docker top ‘container’	# 查看容器内部运行程序
```



容器管理类

```bash
docker exec -it 			# 容器ID sh	进入容器
docker stop ‘container’		# 停止一个正在运行的容器，‘container’可以是容器ID或名称
docker start ‘container’	# 启动一个已经停止的容器
docker restart ‘container’	# 重启容器
docker rm ‘container’		# 删除容器
docker run -i -t -p :80 LAMP /bin/bash	# 运行容器并做http端口转发
docker exec -it ‘container’ /bin/bash	# 进入ubuntu类容器的bash
docker exec -it /bin/sh		# 进入alpine类容器的sh
docker rm docker ps -a -q	# 删除所有已经停止的容器
docker kill $(docker ps -a -q)	# 杀死所有正在运行的容器，$()功能同``
docker pause CONTAINER 		# 暂停容器中所有的进程。
docker unpause CONTAINER 	# 恢复容器中所有的进程。
docker create CONTAINER		# 创建一个新的容器但不启动它
docker commit				# 从容器创建一个新的镜像。
docker cp					# 用于容器与主机之间的数据拷贝。
docker diff 				# 检查容器里文件结构的更改。
```



镜像管理类

```bash
docker login		# 登陆到一个Docker镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hub
docker logout		# 登出一个Docker镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hub
docker login -u 用户名 -p 密码
docker build -t wp-api .		# 构建1个镜像,-t(镜像的名字及标签) wp-api(镜像名) .(构建的目录)
docker run -i -t wp-api			# -t -i以交互伪终端模式运行,可以查看输出信息
docker run -d -p 80:80 wp-api   # -p镜像端口 -d后台模式运行镜像
docker rmi $(docker images -q)	# 删除所有镜像， -f强制删除
docker rmi $(sudo docker images --filter "dangling=true" -q --no-trunc)	# 删除无用镜像
docker images		# 列出本地镜像。
docker history		# 查看指定镜像的创建历史。
docker tag 			# 标记本地镜像，将其归入某一仓库，原标签，新标签
docker save 		# 将指定镜像保存成 tar 归档文件 -o 输出到文件
docker load			# 导入使用 docker save 命令导出的镜像 -i指定导入的文件
docker import		# 从归档文件中创建镜像，和load几乎没有区别

```





### Dockerfile 的语法规则

Dockerfile 包含创建镜像所需要的全部指令。基于在 Dockerfile 中的指令，我们可以使用 `Docker build` 命令来创建镜像。通过减少镜像和容器的创建过程来简化部署。



Dockerfile 支持支持的语法命令如下：

```
INSTRUCTION argument 
```

指令不区分大小写。但是，命名约定为全部大写。

所有 Dockerfile 都必须以 `FROM` 命令开始。`FROM` 命令会指定镜像基于哪个基础镜像创建，接下来的命令也会基于这个基础镜像（注：CentOS 和 Ubuntu 有些命令可是不一样的）。`FROM` 命令可以多次使用，表示会创建多个镜像。具体语法如下：

```
FROM <image name>
```

例如：

```
FROM ubuntu
```

上面的指定告诉我们，新的镜像将基于 Ubuntu 的镜像来构建。

继 `FROM` 命令，DockefFile 还提供了一些其它的命令以实现自动化。在文本文件或 Dockerfile 文件中这些命令的顺序就是它们被执行的顺序。



让我们了解一下这些有趣的 Dockerfile 命令吧。

- MAINTAINER：设置该镜像的作者。语法如下：

  ```
  MAINTAINER <author name> 
  ```

- RUN：在 shell 或者 exec 的环境下执行的命令。`RUN`指令会在新创建的镜像上添加新的层面，接下来提交的结果用在Dockerfile的下一条指令中。语法如下：

  ```
  RUN <command> 
  ```

- ADD：复制文件指令。它有两个参数 source 和 destination。destination 是容器内的路径。source 可以是 URL 或者是启动配置上下文中的一个文件。语法如下：

  ```
  ADD <source> <destination> 
  ```

- CMD：提供了容器默认的执行命令。 Dockerfile 只允许使用一次 CMD 指令。 使用多个 CMD 会抵消之前所有的指令，只有最后一个指令生效。 CMD 有三种形式：

  ```
  CMD ["executable","param1","param2"]
  CMD ["param1","param2"]
  CMD command param1 param2 
  ```

- EXPOSE：指定容器在运行时监听的端口。语法如下：

  ```
  EXPOSE <port>
  ```

- ENTRYPOINT：配置给容器一个可执行的命令，这意味着在每次使用镜像创建容器时一个特定的应用程序可以被设置为默认程序。同时也意味着该镜像每次被调用时仅能运行指定的应用。类似于`CMD`，Docker只允许一个ENTRYPOINT，多个ENTRYPOINT会抵消之前所有的指令，只执行最后的ENTRYPOINT指令。语法如下：

  ```
  ENTRYPOINT ["executable", "param1","param2"]
  ENTRYPOINT command param1 param2 
  ```

- WORKDIR：指定`RUN`、`CMD`与`ENTRYPOINT` 命令的工作目录。语法如下：

  ```
  WORKDIR /path/to/workdir 
  ```

- ENV：设置环境变量。它们使用键值对，增加运行程序的灵活性。语法如下：

  ```
  ENV <key> <value> 
  ```

- USER：镜像正在运行时设置一个 UID。语法如下：

  ```
  USER <uid> 
  ```

- VOLUME：授权访问从容器内到主机上的目录。语法如下：

  ```
  VOLUME ["/data"] 
  ```



### Dockerfile最佳实践

与使用的其他任何应用程序一样，总会有可以遵循的最佳实践。你可以阅读更多有关 Dockerfile 的最佳实践。以下是我们列出的基本的 Dockerfile 最佳实践：

- 保持常见的指令像 MAINTAINER 以及从上至下更新 Dockerfile 命令。
- 当构建镜像时使用可理解的标签，以便更好地管理镜像。
- 避免在 Dockerfile 中映射公有端口。
- CMD 与 ENTRYPOINT 命令请使用数组语法。



### DaoCloud 上的 Dockerfile 编写注意事项

DaoCloud 通过读取 Dockerfile 内容，和来自代码仓库的源代码，为用户构建 Docker 镜像。由于众所周知的原因，国内访问 Docker Hub 的速度令人无法忍受，因此国内常规网络环境下的 Docker 镜像构建速度非常缓慢。DaoCloud 采用非常先进的全球分布式构建引擎，有效缓缓解国内网络问题带来的构建延迟。DaoCloud 兼容 Dockerfile 的所有格式，但是有以下几个注意事项，需要开发者知晓：

- 如您在 Dockerfile 中需要更新 Linux 组件，或安装编程语言的依赖包等，请不要使用国内源，请使用您的 Linux 发行版和编程语言分发机制提供的默认更新源。
- 您可以在构建过程中看到完整的日志文件，如果构建出现问题，日志文件是排错的首选方式。
- 考虑到您的镜像会频繁构建，我们在构建服务器端开启了缓存，之前构建过的 Docker Image Layer 不会重新执行构建，完成和传输的速度也会更快。
- 我们设定了一个构建超时的时间。对于免费用户，构建时间上限是 1 小时，如果 1 小时内您的镜像构建仍未完成（通常是遇到构建问题并死锁），系统将取消您的构建任务；对于付费用户，这个超时时限是 3 小时。