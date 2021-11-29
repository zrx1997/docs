# Gitlab 安装

这里需要安装 10.1.2 版本的 Gitlab，并把数据导入到里面，之后在这里测试 Gitlab 的升级。

## 安装

添加 repo，名为 `/etc/yum.repos.d/gitlab-ce.repo`

```
[gitlab-ce]
name=Gitlab CE Repository
baseurl=https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el$releasever/
gpgcheck=0
enabled=1
```

安装 10.1.2 版本的 gitlab：

```
$ sudo yum makecache
$ sudo yum install gitlab-ce-10.1.2-ce.0.el7.x86_64
```

安装结果：

![image-20200414154343822](https://xujiyou.work/resource/image-20200414154343822.png)

## 修改配置

配置文件是 `/etc/gitlab/gitlab.rb` 。

`external_url` 要确保为正确的ip或者域名，git的链接才正常。 之后就可以通过浏览器访问了，默认是用80端口。

修改备份目录为 `/data1/gitlab/git-backups` 。

修改数据储存目录为 `/data1/gitlab/git-data` 。

全部修改的配置如下：

```
external_url 'http://1.2.3.4:10000'
gitlab_rails['backup_path'] = "/data1/gitlab/git-backups"
gitlab_rails['backup_archive_permissions'] = 0644
gitlab_rails['backup_keep_time'] = 604800
git_data_dirs({ "default" => { "path" => "/data1/gitlab/git-data" } })
gitlab_rails['gitlab_shell_ssh_port'] = 51668
```

604800 秒是 7 天。

然后执行命令。

```
$ sudo gitlab-ctl reconfigure
```

这个命令要执行一段时间。这个命令会把配置保存到 `/var/opt/gitlab` 目录中。

## 目录说明

- `/opt/gitlab` 保存 Gitlab 自身的代码和依赖
- `/var/opt/gitlab` 保存了 `gitlab-ctl reconfigure` 最终写入的配置，
- `/etc/gitlab` 保存了可以人肉编辑的配置和证书。
- `/var/log/gitlab` 保存了 gitlab 的日志。

## 启动

第一次查看状态：

```
$ sudo gitlab-ctl status
```

发现各组件都已经启动了。。。。

这里再启动一下保险：

```
$ sudo gitlab-ctl start
```

其他命令：

```
gitlab-ctl stop
gitlab-ctl restart
gitlab-ctl restart sidekiq
gitlab-rails console
```

查看数据目录发现已经有数据了，备份数据目录还没有数据：

```
$ sudo ls /data1/gitlab/git-data/
$ sudo ls /data1/gitlab/git-backups/
```

## 创建备份

上面的配置已经指定了备份的目录和保存时间，下面来创建备份：

```
$ sudo gitlab-rake gitlab:backup:create
```

再次查看备份目录已经有东西了：

```
$ sudo ls /data1/gitlab/git-backups/
```

上面只是保存了 Gitlab 中的数据，即 Gitlab 中的用户、代码数据，但是没有保存 Gitlab 的配置。下面的脚本用来打包配置：

```
$ sudo sh -c 'umask 0077; tar -cf $(date "+etc-gitlab-%s.tar") -C / etc/gitlab'
```

亲测可行，解包验证：

```
$ sudo tar xvf etc-gitlab-1586852672.tar
```

自动备份：

```
#通过crontab使用备份命令实现自动备份:
0 2 * * * /opt/gitlab/bin/gitlab-rake gitlab:backup:create
```

备份脚本 `/data1/gitlab/git-backups/backup_gitlab.sh` ：

```
#!/bin/bash
#backuping gitlab configurations
back_dir='/data1/gitlab/git-backups/'

date=`date +'%F-%T'`
cd $back_dir
sh -c 'umask 0077; tar -cf $(date "+etc-gitlab-%s.tar") -C / etc/gitlab'
#backup gitlab data & delete old files
/bin/gitlab-rake gitlab:backup:create
find $back_dir -name "*.tar" -mtime +7 | xargs rm -f
#rsync to zfs server
rsync -a --delete --password-file=/root/rsyncd.passwd $back_dir gitlab@4.5.6.7::gitlab
echo "`date +%F-%T` rsync done" >> rsync_gitlab.log
```

这个脚本自动备份配置和数据，并且会自动删除7天前的旧备份。

**rsync命令**是一个远程数据同步工具，可通过LAN/WAN快速同步多台主机间的文件,这个算法只传送两个文件的不同部分，而不是每次都整份传送，因此速度相当快。。

rsync：

- -a 归档模式，表示以递归方式传输文件，并保持所有文件属性。
- --delete 删除那些目标中有，但是源地址中没有的文件。
- --password-file 从FILE中得到密码。

另外这里使用双冒号的原因是：从本地机器拷贝文件到远程rsync服务器中！

最后记录日志。

编辑 `/etc/crontab` 设置定时任务：

```
0 0 * * * root /data1/gitlab/git-backups/backup_gitlab.sh > /dev/null 2>&1
```

这样就实现了每日凌晨0:00 进行全量备份(数据&配置文件),数据保存最近7天,配置文件保存最近7天;

## 修改 root 密码

执行：

```
$ sudo gitlab-rails console production
```

依次输入：

```
 user = User.where(id: 1).first
 user.password="******"
 user.password_confirmation="******"
 user.save!
 quit
```

## 迁移 & 恢复

迁移只比恢复多了一步，就是把数据复制过来。

复制数据时注意，别复制太大的数据，生产环境要小心！！！这里略过复制。

先暂停服务：

```
$ sudo gitlab-ctl stop unicorn
$ sudo gitlab-ctl stop sidekiq
```

再恢复数据：

```
$ sudo gitlab-rake gitlab:backup:restore BACKUP=1586804022_2020_04_14_10.1.2
```

恢复完成后重新启动：

```
$ sudo gitlab-ctl start
```

检查 GitLab 是否正常运行：

```
$ gitlab-rake gitlab:check SANITIZE=true
```

## 去掉注册

管理员账号登录 ----> 进入 `Admin area` (就是那个🔧) ----> `settings` ----> 取消 `Sign-up enabled` ---> `save`







# Gitlab 升级

需要处理 Gitlab 升级的工作。

前同事的部署文档：http://asset.bbdops.com/software/info/e1d4c131-1a30-442c-a15f-c6c84100d79a （仅内网）

目前的版本是 `10.1.2` ，最新版本是 `12.8.5`

官方升级文档：https://docs.gitlab.com/ee/policy/maintenance.html#upgrade-recommendations

## 查看版本号

```
$ cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
10.1.2
```

## 升级版本策略

根据官方升级文档：

![image-20200414141409671](https://xujiyou.work/resource/image-20200414141409671.png)

决定升级路线是 ： `10.1.2` -> `10.8.7` -> `11.11.8` -> `12.0.12` -> `12.8.5` 。共四次升级。

## 升级思路及准备

现在生产环境旁边建一相同版本的测试环境，将数据迁移到测试环境，然后在测试环境进行升级，测试环境升级完成后再进行生产环境的升级。

升级过程中，需要关闭服务，需要提前发邮件约定好。

需要准备好安装包，可以在 https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/ 查找特定版本号的 rpm 包。也可以配置好源，然后用 yum 安装指定版本。

万一生产环境升级失败，服务启动失败，可以直接改 DNS 将测试环境变为生产环境。

下面在测试环境进行升级。

## 升级到 10.8.7

先关闭服务：

```
$ sudo gitlab-ctl stop unicorn
$ sudo gitlab-ctl stop sidekiq
$ sudo gitlab-ctl stop nginx
```

创建数据备份：

```
$ sudo gitlab-rake gitlab:backup:create
```

安装 10.8.7 版本：

```
$ sudo yum install gitlab-ce-10.8.7-ce.0.el7.x86_64
```

重新建立配置：

```
$ sudo gitlab-ctl reconfigure
```

重启：

```
$ sudo gitlab-ctl restart
```

查看状态：

```
$ sudo gitlab-ctl status
```

查看版本号：

```
$ cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
10.8.7
```

网页也能打开并登录，万事大吉。

## 升级到 11.11.8

步骤和上述一致，安装版本换成 11.11.8：

```
$ sudo yum install gitlab-ce-11.11.8-ce.0.el7.x86_64
```

稳定，没毛病。

查看版本号：

```
$ cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
11.11.8
```

## 升级到 12.0.12

按照上面的套路再升级：

```
$ sudo yum install gitlab-ce-12.0.12-ce.0.el7.x86_64
```

查看版本号：

```
$ cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
12.0.12
```

依旧没毛病。

## 升级到 12.8.5

```
$ sudo yum install gitlab-ce-12.8.5-ce.0.el7.x86_64
```

相安无事。。。

```
$ cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
12.8.5
```

## 生产环境升级准备

四次升级，都没有特别注意的地方。备份只需要在关服务后进行一次即可。

产线环境，要把源从本地准备好，网上的源下载太慢，耽误时间。

先把测试环境弄好，包括 CI/DI等。测试没毛病之后，再进行升级。

准备凌晨进行线上环境升级。预计耗时一小时。

## 12.0 版本更新的 CI/CD 功能

在12.0 版本中，Gitlab 对 CI/CD 进行了升级，见官方文档：https://docs.gitlab.com/ee/ci/

需要在机器上安装 gitlab-runner ，官方地址：https://docs.gitlab.com/runner/install/linux-manually.html

可以按照这个地址来安装：https://packages.gitlab.com/runner/gitlab-runner

```
$ curl -s https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
$ sudo yum install gitlab-runner -y
```

安装完成后，进行注册：https://docs.gitlab.com/runner/register/index.html#gnulinux

```
$ sudo gitlab-runner register
```

具体过程如下：

![image-20200415160208230](https://xujiyou.work/resource/image-20200415160208230.png)

这里的地址和 token 要去项目中的 `setting` ---> `CI/CD` ---> `Runners` 中获取。

配置完成后，`gitlab-runner` 会自己启动。。

手动启动，多启动一遍也没啥事：

```
$ sudo gitlab-runner start
```

查看状态：

```
$ sudo gitlab-runner status
```



# Gitlab CI 教程

首先为项目配置 gitlab-runner

可以按照这个地址来安装：https://packages.gitlab.com/runner/gitlab-runner

```
$ curl -s https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
$ sudo yum install gitlab-runner -y
```

安装完成后，进行注册：https://docs.gitlab.com/runner/register/index.html#gnulinux

```
$ sudo gitlab-runner register
```

具体过程如下：

![image-20200415160208230](https://xujiyou.work/Users/jiyouxu/Documents/me/blog/resource/image-20200415160208230.png)

这里的地址和 token 要去项目中的 `setting` ---> `CI/CD` ---> `Runners` 中获取。

配置完成后，`gitlab-runner` 会自己启动。。

手动启动，多启动一遍也没啥事：

```
$ sudo gitlab-runner start
```

查看状态：

```
$ sudo gitlab-runner status
```

## .gitlab-ci.yaml 文件

我这里的最简文件：

```
# 定义 stages
stages:
  - test

# 定义 job
job1:
  stage: test
  script:
    - echo "I am job1" >> /home/gitlab-runner/job1.txt
    - echo "I am in test stage" >> /home/gitlab-runner/jjob1.txt
  tags:
    - fueltank
```

主要就是学习这个配置文件怎么写。

## 原理

gitlab-runner 一直在后台 pull 代码，一遇到 commit 就执行 `.gitlab-ci.yaml` 这里面定义好的命令。

### 配置 Runner

Runner 用来运行 Pipeline，Runner 可以是 ssh、docker 等类型，推荐使用隔离性更好的 docker。默认已经配置好一个所有项目公用的 Shared Runner，如有需要可为 Group 和 Project 创建单独的 Runner。

### 配置 Variables

有些值，比如 Docker Registry 帐号、Kubernetes 集群访问密钥等，不方便直接写死在 Pipeline 定义文件中，可现在 Group 或 Project 上定义好。GitLab 本身已内置许多变量 [Predefined environment variables reference](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)。

### 定义 Pipeline

Pipeline 用来描述持续集成和持续部署的具体过程，它由一个个顺序执行的 Stage 构成，每个 Stage 包含一到多个并行执行的 Job。下面是一个 Java Spring Boot 服务的 Pipeline 示例：

```
stages:
  - build
  - package
  - deploy

maven-build:
  stage: build
  only:
    refs:
      - dev
      - test
      - master
  image: registry.prod.bbdops.com/common/maven:3.6.3-jdk-8
  variables:
    MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository -Dmaven.test.skip=true "
    MAVEN_CLI_OPTS: "-s .m2/settings.xml --batch-mode"
  script:
    - mvn $MAVEN_CLI_OPTS package
  artifacts:
    paths:
      - target/*.jar
  cache:
    paths:
      - .m2/repository/

docker-build:
  stage: package
  image: registry.prod.bbdops.com/common/docker:19.03.8
  services:
    - name: registry.prod.bbdops.com/common/docker:19.03.8-dind
      alias: docker
      command: ["--insecure-registry=registry.prod.bbdops.com", "--registry-mirror=https://nypkinfs.mirror.aliyuncs.com"]
  variables:
    DOCKER_IMAGE_NAME: appone/canghai-user
  script:
    - echo $BBD_DOCKER_REGISTRY_PASSWORD | docker login -u $BBD_DOCKER_REGISTRY_USERNAME --password-stdin $BBD_DOCKER_REGISTRY
    - docker pull $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:latest || true
    - docker build --cache-from $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:latest -t $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$CI_COMMIT_SHORT_SHA -t $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$CI_COMMIT_BRANCH -t $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:latest .
    - docker push $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$CI_COMMIT_SHORT_SHA
    - docker push $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$CI_COMMIT_BRANCH
    - docker push $BBD_DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:latest

.kubernetes-deploy:
  stage: deploy
  image: registry.prod.bbdops.com/common/google/cloud-sdk:289.0.0
  script:
    - sed -i 's/$CI_COMMIT_SHORT_SHA/'"$CI_COMMIT_SHORT_SHA"'/' deployment.yml
    - kubectl apply -f deployment.yml -n canghai

kubernetes-deploy-development:
  extends: .kubernetes-deploy
  only:
    refs:
      - dev
  before_script:
    - cat $KUBERNETES_DEVELOPMENT_CLUSTER_CONFIG >~/.kube/config

kubernetes-deploy-testing:
  extends: .kubernetes-deploy
  only:
    refs:
      - test
  before_script:
    - cat $KUBERNETES_TESTING_CLUSTER_CONFIG >~/.kube/config

kubernetes-deploy-production:
  extends: .kubernetes-deploy
  only:
    refs:
      - master
  when: manual
  before_script:
    - cat $KUBERNETES_PRODUCTION_CLUSTER_CONFIG >~/.kube/config
```

如果是前端项目，可替换其中的 `maven-build` 任务为如下的 `node-build`。

```
node-build:
  stage: build
  only:
    refs:
      - dev
      - test
      - master
  image: registry.prod.bbdops.com/common/node:12.16.3
  variables:
    CACHE_FOLDER: .yarn
  script:
    - yarn config set cache-folder $CACHE_FOLDER
    - yarn install --registry http://verdaccio.bbdops.com/
    - yarn run build
  artifacts:
    paths:
      - build/
  cache:
    paths:
      - $CACHE_FOLDER
```

### 触发 Pipeline

Push 代码到某个分支即可自动触发跟该分支相关的 Job，也可在项目 CI/CD 页手动触发 Pipeline 或者重试某个 Job，还可创建 Schedule 来定时触发。