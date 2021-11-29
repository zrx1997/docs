记录一些用过的 Nginx 配置。

------

## Nginx 代理 Vue.js 静态网站

```
   server {
        listen       80;
        server_name     boot.serrhub.com;
        location / {
            root /opt/source/serrhub-front/dist;
            index index.html;
            add_header Access-Control-Allow-Origin *;
            try_files $uri $uri/ /index.html;
        }
    }
```

## Nginx 代理 Hexo 静态网站

```
    server {
        listen       443 ssl;
        server_name  xujiyou.work www.xujiyou.work;

        ssl_certificate "/etc/nginx/conf.d/cret/xujiyou-work-nginx-1214113354/xujiyou.work_chain.crt";
        ssl_certificate_key "/etc/nginx/conf.d/cret/xujiyou-work-nginx-1214113354/xujiyou.work_key.key";
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        location /README/index.html {
            root /opt/public/;
            index index.html;
            add_header Access-Control-Allow-Origin *;
        }

        location ^~/README/ {
            proxy_set_header Host $host;
            proxy_set_header  X-Real-IP        $remote_addr;
            proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_set_header X-NginX-Proxy true;
            #rewrite ^/README/(.*)$ /$1 break;
            if ($request_uri ~* \.md$) {
               rewrite ^/(.*)\.md$ /$1 break;
            }
            proxy_pass http://README/;
        }

        location ~ ^/.*/resource/.*$ {
            rewrite ^/(.*)/resource/(.*)$ https://xujiyou.work/resource/$2 break;
        }

        location / {
            root /opt/public/;
            index index.html;
            add_header Access-Control-Allow-Origin *;
           # try_files $uri $uri/ /index.html;
            if ( $request_uri = "/" ) {
                rewrite "/" https://xujiyou.work/README/index.html break;
            }
        }


        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```

## Nginx 代理 Java 服务

```
    server {
        listen       443 ssl;
        server_name  boot.xujiyou.work;

        ssl_certificate "/etc/nginx/conf.d/cret/boot-xujiyou-work-nginx-1216114456/boot.xujiyou.work_chain.crt";
        ssl_certificate_key "/etc/nginx/conf.d/cret/boot-xujiyou-work-nginx-1216114456/boot.xujiyou.work_key.key";
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
```

## 设置上传大小

```
server {
        listen        80;
        server_name    www.S1.com;
        client_max_body_size 30M;

        location /api/ {
            proxy_pass http://127.0.0.1:8891/;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_send_timeout 3600s;
            proxy_read_timeout 3600s;
            proxy_connect_timeout 60s;
        }

        location / {
            root /opt/s1/www.S1.com;
            index index.html;
            add_header Access-Control-Allow-Origin *;
            try_files $uri $uri/ /index.html;
        }
    }
```

如果 proxy_pass的结尾有`/`， 则会把`/api/*`后面的路径直接拼接到后面，即移除api.

## 404 重写

```
        location / {
            root   /data1/imgs;
            autoindex on;

            if ($request_uri ~* ^/all) {
                error_page 404 =200 @test;
            }

            if ($request_uri ~* ^/test) {
                error_page 404 =200 @minio;
            }

        }

        location @test {
            rewrite ^/all/(.*)$ /test/$1 permanent;
        }

        location @minio {
            rewrite ^/test/(.*)$ http://192.168.6.124:29000/test/$1 permanent;
        }
```

## 跨域

```
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Headers x-token,Token,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization;
    add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
```

## Nginx 配置 WebSocket

```
        location ~*  ^/monitor/ws/.* {
            rewrite ^/monitor(.*)$ $1 break;
            add_header Access-Control-Allow-Origin *;
            proxy_pass http://127.0.0.1:8003;
            proxy_set_header Host $http_host;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
```





Nginx 官方文档：http://nginx.org/en/docs/

二进制安装文档：http://nginx.org/en/docs/configure.html

最新标准版为 1.18，下载地址是：http://nginx.org/en/download.html

## Nignx编译安装

安装编译环境：

```
$ yum -y install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel
```

创建用户：

```
$ useradd -r nginx
```

配置：

```
$ ./configure \
    --user=root \
    --group=root \
    --prefix=/usr/local/nginx/ \
    --sbin-path=/usr/bin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx/nginx.pid \
    --lock-path=/var/run/nginx/nginx.lock \
    --http-client-body-temp-path=/var/lib/nginx/client_body_temp \
    --http-proxy-temp-path=/var/lib/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/lib/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/lib/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/lib/nginx/scgi_temp \
    --with-http_ssl_module
```

编译：

```
$ make
```

安装：

```
$ make install
```

验证：

```
$ nginx -V
```

返回了安装时配置的参数，这些参数配置是卸载 Nginx 时的依据。

### 启动

创建目录并赋予权限：

```
$ sudo mkdir /var/lib/nginx
$ sudo chown -R nginx:nginx /etc/nginx/
$ sudo chown -R nginx:nginx /var/lib/nginx
$ sudo chown -R nginx:nginx /var/run/nginx
$ sudo chown -R nginx:nginx /var/log/nginx
```

创建 `/usr/lib/systemd/system/nginx.service` ：

```
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/nginx/nginx.pid
# Nginx will fail to start if /run/nginx.pid already exists but has the wrong
# SELinux context. This might happen when running `nginx -t` from the cmdline.
# https://bugzilla.redhat.com/show_bug.cgi?id=1268621
ExecStartPre=/usr/bin/rm -f /var/run/nginx/nginx.pid
ExecStartPre=/usr/bin/nginx -t
ExecStart=/usr/bin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
KillSignal=SIGQUIT
TimeoutStopSec=5
KillMode=process
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

启动 Nginx：

```
$ sudo systemctl enable nginx
$ sudo systemctl start nginx
```

### 总结

上面这套步骤和 yum 安装的没有很大差别，源码安装的好处在于可以自定义，可以灵活选择版本、模块。

# Nginx 进程模型

Nginx 采用的是多进程（单线程） & 多路IO复用模型。使用了 I/O 多路复用技术的 Nginx，就成了”并发事件驱动“的服务器。

Nginx的master-worker进程模型是其能够高性能的处理用户请求的原因之一，而且这里的每个worker进程都只会启动一个线程来处理用户请求。通常我们会将worker进程的数量设置得与我们的CPU数量一致，nginx也会将每个进程与每个CPU进行绑定。通过这种方式，可以充分利用操作系统多核的特性，并且能够最大限度的减少线程之间的切换而导致的资源损耗。除此之外，进程之间是相互独立的，一个 worker 进程挂了不会影响到其他 worker 进程。

## 配置nginx绑定CPU

刚才说nginx除外，是因为nginx提供了更精确的控制。

在*conf/nginx.conf*中，有如下一行：

```
worker_processes  1;
```

这是用来配置nginx启动几个工作进程的，默认为1。而nginx还支持一个名为worker_cpu_affinity的配置项，也就是说，nginx可以为**每个工作进程绑定CPU**。我做了如下配置：

```
worker_processes  3;
worker_cpu_affinity 0010 0100 1000;
```

这里0010 0100 1000是掩码，分别代表第2、3、4颗cpu核心。

重启nginx后，3个工作进程就可以各自用各自的CPU了。

## 工作原理

![这里写图片描述](https://xujiyou.work/resource/SouthEast.png)

1. Nginx 在启动后，会有一个 master 进程和多个相互独立的 worker 进程。
2. 接收来自外界的信号，向各worker进程发送信号，每个进程都有可能来处理这个连接。
3. master 进程能监控 worker 进程的运行状态，当 worker 进程退出后(异常情况下)，会自动启动新的 worker 进程。

## 惊群现象

主进程（master 进程）首先通过 socket() 来创建一个 sock 文件描述符用来监听，然后fork生成子进程（workers 进程），子进程将继承父进程的 sockfd（socket 文件描述符），之后子进程 accept() 后将创建已连接描述符（connected descriptor）），然后通过已连接描述符来与客户端通信。

那么，由于所有子进程都继承了父进程的 sockfd，那么当连接进来时，所有子进程都将收到通知并“争着”与它建立连接，这就叫“惊群现象”。大量的进程被激活又挂起，只有一个进程可以accept() 到这个连接，这当然会消耗系统资源。

#### Nginx对惊群现象的处理

Nginx 提供了一个 accept_mutex 这个东西，这是一个加在accept上的一把互斥锁。即每个 worker 进程在执行 accept 之前都需要先获取锁，获取不到就放弃执行 accept()。有了这把锁之后，同一时刻，就只会有一个进程去 accpet()，这样就不会有惊群问题了。accept_mutex 是一个可控选项，我们可以显示地关掉，默认是打开的。

## worker进程工作流程

当一个 worker 进程在 accept() 这个连接之后，就开始读取请求，解析请求，处理请求，产生数据后，再返回给客户端，最后才断开连接，一个完整的请求。一个请求，完全由 worker 进程来处理，而且只能在一个 worker 进程中处理。

这样做带来的好处：

1. 节省锁带来的开销。每个 worker 进程都是独立的进程，不共享资源，不需要加锁。同时在编程以及问题查上时，也会方便很多。
2. 独立进程，减少风险。采用独立的进程，可以让互相之间不会影响，一个进程退出后，其它进程还在工作，服务不会中断，master 进程则很快重新启动新的 worker 进程。当然，worker 进程的也能发生意外退出。

多进程模型每个进程/线程只能处理一路IO，那么 Nginx是如何处理多路IO呢？

如果不使用 IO 多路复用，那么在一个进程中，同时只能处理一个请求，比如执行 accept()，如果没有连接过来，那么程序会阻塞在这里，直到有一个连接过来，才能继续向下执行。

而多路复用，允许我们只在事件发生时才将控制返回给程序，而其他时候内核都挂起进程，随时待命。

#### 核心：Nginx采用的 IO多路复用模型epoll

epoll 通过在 Linux 内核中申请一个简易的文件系统（文件系统一般用什么数据结构实现？B+树），其工作流程分为三部分：

1. 调用 int epoll_create(int size)建立一个epoll对象，内核会创建一个eventpoll结构体，用于存放通过epoll_ctl()向epoll对象中添加进来的事件，这些事件都会挂载在红黑树中。
2. 调用 int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event) 在 epoll 对象中为 fd 注册事件，所有添加到epoll中的事件都会与设备驱动程序建立回调关系，也就是说，当相应的事件发生时会调用这个sockfd的回调方法，将sockfd添加到eventpoll 中的双链表。
3. 调用 int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout) 来等待事件的发生，timeout 为 -1 时，该调用会阻塞直到有事件发生

这样，注册好事件之后，只要有 fd 上事件发生，epoll_wait() 就能检测到并返回给用户，用户就能”非阻塞“地进行 I/O 了。

epoll() 中内核则维护一个链表，epoll_wait 直接检查链表是不是空就知道是否有文件描述符准备好了。（epoll 与 select 相比最大的优点是不会随着 sockfd 数目增长而降低效率，使用 select() 时，内核采用轮训的方法来查看是否有fd 准备好，其中的保存 sockfd 的是类似数组的数据结构 fd_set，key 为 fd，value 为 0 或者 1。）

能达到这种效果，是因为在内核实现中 epoll 是根据每个 sockfd 上面的与设备驱动程序建立起来的回调函数实现的。那么，某个 sockfd 上的事件发生时，与它对应的回调函数就会被调用，来把这个 sockfd 加入链表，其他处于“空闲的”状态的则不会。在这点上，epoll 实现了一个”伪”AIO。但是如果绝大部分的 I/O 都是“活跃的”，每个 socket 使用率很高的话，epoll效率不一定比 select 高（可能是要维护队列复杂）。

可以看出，因为一个进程里只有一个线程，所以一个进程同时只能做一件事，但是可以通过不断地切换来“同时”处理多个请求。

例子：Nginx 会注册一个事件：“如果来自一个新客户端的连接请求到来了，再通知我”，此后只有连接请求到来，服务器才会执行 accept() 来接收请求。又比如向上游服务器（比如 PHP-FPM）转发请求，并等待请求返回时，这个处理的 worker 不会在这阻塞，它会在发送完请求后，注册一个事件：“如果缓冲区接收到数据了，告诉我一声，我再将它读进来”，于是进程就空闲下来等待事件发生。

这样，基于 **多进程+epoll**， Nginx 便能实现高并发。

## Nginx 与 多进程模式 Apache 的比较：

事件驱动适合于I/O密集型服务，多进程或线程适合于CPU密集型服务： 1、Nginx 更主要是作为反向代理，而非Web服务器使用。其模式是事件驱动。 2、事件驱动服务器，最适合做的就是这种 I/O 密集型工作，如反向代理，它在客户端与WEB服务器之间起一个数据中转作用，纯粹是 I/O 操作，自身并不涉及到复杂计算。因为进程在一个地方进行计算时，那么这个进程就不能处理其他事件了。 3、Nginx 只需要少量进程配合事件驱动，几个进程跑 libevent，不像 Apache 多进程模型那样动辄数百的进程数。 5、Nginx 处理静态文件效果也很好，那是因为读写文件和网络通信其实都是 I/O操作，处理过程一样。