### GitLab简介

​	GitLab 是一个用于仓库管理系统的开源项目。使用Git作为代码管理工具，并在此基础上搭建起来的web服务。可通过Web界面进行访问公开的或者私人项目。它拥有与Github类似的功能，能够浏览源代码，管理缺陷和注释。可以管理团队对仓库的访问，它非常易于浏览提交过的版本并提供一个文件历史库。团队成员可以利用内置的简单聊天程序(Wall)进行交流。它还提供一个代码片段收集功能可以轻松实现代码复用。

常用的网站：
	官网：https://about.gitlab.com/
	国内镜像：https://mirrors.tuna.tsinghua.edu.cn/gitlab‐ce/yum/



### 基本要求：

```
    1、 CentOS 7.x
    2、 生产（至少4G），建议8G，存储最低100G
    3、 安装包：gitlab‐ce‐10.2.2‐ce
    4、 禁用防火墙，关闭selinux
```



### 使用规范：

```
	gitlab是一个开源的git服务软件，与大名鼎鼎的github所提供的功能类似，适合企业或团队搭建属于自己的在线git仓库。
	整个IT部门使用一套gitlab，很好的结合容器云平台自动CI/CD，流水线管理。在使用过程中，为了避免不同团队之间使用存在不规范，因此提出了一些必要的规范约束。

    1、建议使用ssh协议访问仓库。
    2、利用分组（Groups）进行管理权限。
    3、必须写README.MD，描述项目整体。
    4、签入代码描述准确。
    5、保护master分支，git工程的master分支一般比较重要，默认master是保护状态，对分支合并主干的代码进行评审，由专门技术负责人将分支合并master。
  
```

#### 权限管理

```
针对于不同的使用人员，给于不同的权限
	Owner 项目所有者，拥有所有的操作权限
    Master 项目的管理者，除更改、删除项目元信息外其它操作均可
    Developer 项目的开发人员，做一些开发工作，对受保护内容无权限
    Reporter 项目的报告者，只有项目的读权限，可以创建代码片断
    Guest 项目的游客，只能提交问题和评论内容
```



#### 分支管理

```
	每次提交必须写明注释，如果是修复Bug，请指明修复了哪些bug
    Git主分支的名字，默认叫做Master。它是自动建立的，版本库初始化以后，默认就是在主分支在进行开发。
    主分支只用来分布重大版本，日常开发应该在另一条分支上完成。我们把开发用的分支，叫做Develop。
    除了常设分支以外，还有一些临时性分支，用于应对一些特定目的的版本开发。临时性分支主要有三种：
    　　* 功能（feature）分支
　　	  * 预发布（release）分支
　　    * 修补bug（fixbug）分支
　　这三种分支都属于临时性需要，使用完以后，应该删除，使得代码库的常设分支始终只有Master和Develop。
```



#### 合并管理

```
	合并分支时必须使用--no-ff参数（禁止以快进方式合并），以保留合并历史轨迹
	注意与主仓库的同步，保持一定的fetch频率。防止出现长时间不同步而冲突严重的情况。
	如果发起合并时发现有冲突，可自己撤回手动解决冲突后再重新发起。
	向主仓库发起合并不要过于频繁
```



### 安装部署：

```bash
# 安装基本依赖包
	yum install ‐y curl policycoreutils‐python openssh‐server
	cd /home/adcwb/tools
# 上传gitlab安装包 下载方式可通过国内清华源gitlab‐ce社区版本下载
	rz ‐bye gitlab‐ce‐10.2.2‐ce.0.el7.x86_64.rpm 
# gitlab 配置文件
	vim /etc/gitlab/gitlab.rb 
		external_url 'http://10.0.0.203'	# 更改url地址为本机IP地址 
# 更改配置文件后需重新配置
	gitlab‐ctl reconfigure
	
# gitlab常用目录
    /opt/gitlab/ # gitlab的程序安装目录
    /var/opt/gitlab # gitlab目录数据目录
    /var/opt/gitlab/git‐dfata # 存放仓库数据

# gitlab常用指令
    gitlab‐ctl status # 查看目前gitlab所有服务运维状态
    gitlab‐ctl stop # 停止gitlab服务
    gitlab‐ctl stop nginx # 单独停止某个服务
    gitlab‐ctl tail # 查看所有服务的日志
    
# Gitlab的服务构成：
    nginx： 静态web服务器
    gitlab‐workhorse: 轻量级的反向代理服务器
    logrotate：日志文件管理工具
    postgresql：数据库
    redis：缓存数据库
    sidekiq：用于在后台执行队列任务（异步执行）。（Ruby）
    unicorn：An HTTP server for Rack applications，GitLab Rails应用是托管在这个服务器上面的。（Ruby
    Web Server,主要使用Ruby编写）
```





### gitlab汉化：

```
1、下载汉化补丁
	git clone https://gitlab.com/xhang/gitlab.git
2、查看全部分支版本
	git branch ‐a
3、对比版本、生成补丁包
	git diff remotes/origin/10‐2‐stable remotes/origin/10‐2‐stable‐zh > ../10.2.2‐zh.diff
4、停止服务器
	gitlab‐ctl stop
5、打补丁
	patch ‐d /opt/gitlab/embedded/service/gitlab‐rails ‐p1 < /tmp/10.2.2‐zh.diff
6、启动和重新配置
	gitlab‐ctl start
	gitlab‐ctl reconfigure
```



### gitlab使用

```
1、配置外观
	管理区域‐外观
2、关闭自动注册‐可根据实际需求操作
	管理区域‐设置‐关闭自动注册
3、创建组‐用户‐项目
	创建组
```



### gitlab备份

```bash
	对gitlab进行备份将会创建一个包含所有库和附件的归档文件。对备份的恢复只能恢复到与备份时的gitlab相同的版本。将gitlab迁移到另一台服务器上的最佳方法就是通过备份和还原。

	gitlab提供了一个简单的命令行来备份整个gitlab，并且能灵活的满足需求。

	备份文件将保存在配置文件中定义的backup_path中，文件名为TIMESTAMP_gitlab_backup.tar,TIMESTAMP为备份时的时间戳。TIMESTAMP的格式为：EPOCH_YYYY_MM_DD_Gitlab-version。
	
	如果自定义备份目录需要赋予git权限
	配置文件中加入/etc/gitlab/gitlab.rb
		gitlab_rails['backup_path'] = '/data/backup/gitlab'
		gitlab_rails['backup_keep_time'] = 604800       备份保留的时间（以秒为单位，这个是七天默认值），
	mkdir /data/backup/gitlab
	chown -R git.git /data/backup/gitlab
	完成后执行gitlab-ctl reconfigure

```



#### 手动备份

​	执行：gitlab-rake gitlab:backup:create生成一次备份。

```
[root@node2 ~]# gitlab-rake gitlab:backup:create
Dumping database ... 
Dumping PostgreSQL database gitlabhq_production ... [DONE]
done
Dumping repositories ...
 * web-site/frontend ... [DONE]
 * web-site/frontend.wiki ...  [SKIPPED]
 * web-site/backend ... [SKIPPED]
 * web-site/backend.wiki ...  [SKIPPED]
 * devops/accout ... [DONE]
 * devops/accout.wiki ...  [SKIPPED]
 * devops/user ... [DONE]
 * devops/user.wiki ...  [SKIPPED]
 * web-site/accout ... [DONE]
 * web-site/accout.wiki ...  [SKIPPED]
done
Dumping uploads ... 
done
Dumping builds ... 
done
Dumping artifacts ... 
done
Dumping pages ... 
done
Dumping lfs objects ... 
done
Dumping container registry images ... 
[DISABLED]
Creating backup archive: 1512811475_2017_12_09_10.2.2_gitlab_backup.tar ... done
Uploading backup archive to remote storage  ... skipped
Deleting tmp directories ... done
done
done
done
done
done
done
done
Deleting old backups ... skipping
[root@node2 ~]# ll /var/opt/gitlab/backups/
total 272
-rw------- 1 git git 276480 Dec  9 17:24 1512811475_2017_12_09_10.2.2_gitlab_backup.tar

```

#### 定时备份

​	在定时任务里添加：

​		0 2 * * * /opt/gitlab/bin/gitlab-rake gitlab:backup:create CRON=1

​	环境变量CRON=1的作用是如果没有任何错误发生时， 抑制备份脚本的所有进度输出。



### gitlab恢复

​	只能还原到与备份文件相同的gitlab版本。

​	执行恢复操作时，需要gitlab处于运行状态，备份文件位于gitlab_rails['backup_path']。

```
[root@node2 ~]# ll /var/opt/gitlab/backups/
total 272
-rw------- 1 git git 276480 Dec  9 17:24 1512811475_2017_12_09_10.2.2_gitlab_backup.tar

```

​	停止连接到数据库的进程（也就是停止数据写入服务），但是保持GitLab是运行的。

```
[root@node2 ~]# gitlab-ctl stop unicorn
ok: down: unicorn: 0s, normally up
[root@node2 ~]# gitlab-ctl stop sidekiq
ok: down: sidekiq: 0s, normally up
确认：
[root@node2 ~]# gitlab-ctl status
run: gitaly: (pid 1497) 0s; run: log: (pid 540) 0s
run: gitlab-monitor: (pid 1507) 0s; run: log: (pid 543) 0s
run: gitlab-workhorse: (pid 1517) 0s; run: log: (pid 508) 0s
run: logrotate: (pid 14405) 1564s; run: log: (pid 510) 0s
run: nginx: (pid 1532) 0s; run: log: (pid 507) 0s
run: node-exporter: (pid 1538) 0s; run: log: (pid 525) 0s
run: postgres-exporter: (pid 1543) 0s; run: log: (pid 530) 0s
run: postgresql: (pid 1551) 0s; run: log: (pid 492) 0s
run: prometheus: (pid 1559) 0s; run: log: (pid 535) 0s
run: redis: (pid 1567) 0s; run: log: (pid 491) 0s
run: redis-exporter: (pid 1572) 0s; run: log: (pid 547) 0s
down: sidekiq: 121s, normally up; run: log: (pid 500) 0s
down: unicorn: 133s, normally up; run: log: (pid 502) 0s
```

​	接下进行恢复，指定时间戳你要从那个备份恢复：

```BASH
[root@node2 ~]# gitlab-rake gitlab:backup:restore BACKUP=1512811475_2017_12_09_10.2.2
Unpacking backup ... done
Before restoring the database, we will remove all existing
tables to avoid future upgrade problems. Be aware that if you have
custom tables in the GitLab database these tables and all data will be
removed.

Do you want to continue (yes/no)? 
将移除我们自建的表。回答yes
Restoring uploads ... 
done
Restoring builds ... 
done
Restoring artifacts ... 
done
Restoring pages ... 
done
Restoring lfs objects ... 
done
This will rebuild an authorized_keys file.
You will lose any data stored in authorized_keys file.
Do you want to continue (yes/no)? 
将移除所有的认证Key。回答yes
....
Deleting tmp directories ... done
done
done
done
done
done
done
done

完成后重启GitLab服务
[root@node2 ~]# gitlab-ctl restart
ok: run: gitaly: (pid 18194) 0s
ok: run: gitlab-monitor: (pid 18204) 0s
ok: run: gitlab-workhorse: (pid 18209) 1s
ok: run: logrotate: (pid 18224) 0s
ok: run: nginx: (pid 18231) 1s
ok: run: node-exporter: (pid 18237) 0s
ok: run: postgres-exporter: (pid 18242) 0s
ok: run: postgresql: (pid 18314) 0s
ok: run: prometheus: (pid 18317) 1s
ok: run: redis: (pid 18326) 0s
ok: run: redis-exporter: (pid 18330) 0s
ok: run: sidekiq: (pid 18345) 0s
ok: run: unicorn: (pid 18354) 0s

检查GitLab的服务
[root@node2 ~]# gitlab-rake gitlab:check SANITIZE=true
Checking GitLab Shell ...

GitLab Shell version >= 5.9.4 ? ... OK (5.9.4)
Repo base directory exists?
default... yes
Repo storage directories are symlinks?
default... no
Repo paths owned by git:root, or git:git?
default... yes
Repo paths access is drwxrws---?
default... yes
hooks directories in repos are links: ... 
2/3 ... ok
2/4 ... repository is empty
7/5 ... ok
7/7 ... ok
2/8 ... ok
Running /opt/gitlab/embedded/service/gitlab-shell/bin/check
Check GitLab API access: OK
Redis available via internal API: OK

Access to /var/opt/gitlab/.ssh/authorized_keys: OK
gitlab-shell self-check successful

Checking GitLab Shell ... Finished

Checking Sidekiq ...

Running? ... yes
Number of Sidekiq processes ... 1

Checking Sidekiq ... Finished

Reply by email is disabled in config/gitlab.yml
Checking LDAP ...

LDAP is disabled in config/gitlab.yml

Checking LDAP ... Finished

Checking GitLab ...

Git configured correctly? ... yes
Database config exists? ... yes
All migrations up? ... yes
Database contains orphaned GroupMembers? ... no
GitLab config exists? ... yes
GitLab config up to date? ... yes
Log directory writable? ... yes
Tmp directory writable? ... yes
Uploads directory exists? ... yes
Uploads directory has correct permissions? ... yes
Uploads directory tmp has correct permissions? ... skipped (no tmp uploads folder yet)
Init script exists? ... skipped (omnibus-gitlab has no init script)
Init script up-to-date? ... skipped (omnibus-gitlab has no init script)
Projects have namespace: ... 
2/3 ... yes
2/4 ... yes
7/5 ... yes
7/7 ... yes
2/8 ... yes
Redis version >= 2.8.0? ... yes
Ruby version >= 2.3.5 ? ... yes (2.3.5)
Git version >= 2.7.3 ? ... yes (2.13.6)
Git user has default SSH configuration? ... yes
Active users: ... 5

Checking GitLab ... Finished

```



