

### Socket层：

![image-20200813153138546](2、socket编程.assets/image-20200813153138546.png)

```
Socket层：
    Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口
    在设计模式中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。
    程序的pid：同一台机器上不同进程或者线程的标识

套接字：
    什么是套接字：
        一开始,套接字被设计用在同 一台主机上多个应用程序之间的通讯。这也被称进程间通讯,或 IPC。套接字有两种（或者称为有两个种族）,分别是基于文件型的和基于网络型的。
    发展史：
        套接字起源于 20 世纪 70 年代加利福尼亚大学伯克利分校版本的 Unix,即人们所说的 BSD Unix。 因此,有时人们也把套接字称为“伯克利套接字”或“BSD 套接字”
    基于文件类型的套接字家族：
        AF_UNIX
            unix一切皆文件，基于文件的套接字调用的就是底层的文件系统来取数据，两个套接字进程运行在同一机器，可以通过访问同一个文件系统间接完成通信
    基于网络类型的套接字家族：
        AF_INET
(还有AF_INET6被用于ipv6，还有一些其他的地址家族，不过，他们要么是只用于某个平台，要么就是已经被废弃，或者是很少被使用，或者是根本没有实现，所有地址家族中，AF_INET是使用最广泛的一个，python支持很多种地址家族，但是由于我们只关心网络编程，所以大部分时候我么只使用AF_INET)


```

### 套接字的工作流程：

![image-20200810213403901](2、socket编程.assets/image-20200810213403901.png)

### 常用的套接字函数

```python
服务端套接字函数
    s.bind()    绑定(主机,端口号)到套接字
    s.listen()  开始TCP监听
    s.accept()  被动接受TCP客户的连接,(阻塞式)等待连接的到来

客户端套接字函数
    s.connect()     主动初始化TCP服务器连接
    s.connect_ex()  connect()函数的扩展版本,出错时返回出错码,而不是抛出异常

公共用途的套接字函数
    s.recv()            接收TCP数据
    s.send()            发送TCP数据(send在待发送数据量大于己端缓存区剩余空间时,数据丢失,不会发完)
    s.sendall()         发送完整的TCP数据(本质就是循环调用send,sendall在待发送数据量大于己端缓存区剩余空间时,数据不丢失,循环调用send直到发完)
    s.recvfrom()        接收UDP数据
    s.sendto()          发送UDP数据
    s.getpeername()     连接到当前套接字的远端的地址
    s.getsockname()     当前套接字的地址
    s.getsockopt()      返回指定套接字的参数
    s.setsockopt()      设置指定套接字的参数
    s.close()           关闭套接字

面向锁的套接字方法
    s.setblocking()     设置套接字的阻塞与非阻塞模式
    s.settimeout()      设置阻塞套接字操作的超时时间
    s.gettimeout()      得到阻塞套接字操作的超时时间

面向文件的套接字的函数
    s.fileno()          套接字的文件描述符
    s.makefile()        创建一个与该套接字相关的文件
```

### 案例：模拟打电话过程(TCP套接字)

```python
Server

    import socket

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 先生产一部手机
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 让手机卡可以重复使用
    ip_port = ("127.0.0.1", 10000)  # 手机卡
    sk.bind(ip_port)  # 插入手机卡
    sk.listen(5)  # 手机待机

    while True:                             # 新增接收链接循环,可以不停的接电话

        conn, addr = sk.accept()  # 手机接电话
        """
        print(conn)

                <socket.socket fd=548,
                family=AddressFamily.AF_INET, 
                type=SocketKind.SOCK_STREAM, 
                proto=0, 
                laddr=('127.0.0.1', 10000), 
                raddr=('127.0.0.1', 32726)>
        print(addr)  # ('127.0.0.1', 32726)
        """
        print('接到来自%s的电话' % addr[0])
        while True:
            msg = conn.recv(1024)  # 听消息，每次能听到1024个字节数据
            print(msg.decode())  # 默认是字节流
            data = input("请输入要回复的消息：")
            conn.send(data.encode())  # 讲话
            if data.upper() == "Q":
                break
    conn.close()  # 挂电话
    sk.close()  # 手机关机，释放电话卡


```

```pytohn
Client

    import socket

    ip_port = ("127.0.0.1", 10000)            # 手机卡
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sk.connect(ip_port)                       # 拨电话
    while True:
        strvar = input("请输入您要发送的内容：")
        sk.send(strvar.encode())
        res = sk.recv(1024)
        if res == b"q" or res == b"Q":
            break
        print(res.decode())

    sk.close()                                  #关机
```



### 端口占用问题解决方案

```python
方案一：
	#加入一条socket配置，重用ip和端口
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 在bind前加
  
方案二：
	发现系统存在大量TIME_WAIT状态的连接，通过调整linux内核参数解决，
    vi /etc/sysctl.conf

    编辑文件，加入以下内容：
    net.ipv4.tcp_syncookies = 1
    net.ipv4.tcp_tw_reuse = 1
    net.ipv4.tcp_tw_recycle = 1
    net.ipv4.tcp_fin_timeout = 30
 
    然后执行 /sbin/sysctl -p 让参数生效。
    
参数解释：
    net.ipv4.tcp_syncookies = 1 
            表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；
    net.ipv4.tcp_tw_reuse = 1 
            表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；
    net.ipv4.tcp_tw_recycle = 1 
            表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。
    net.ipv4.tcp_fin_timeout 
            修改系統默认的 TIMEOUT 时间
```

### 案例二：QQ聊天 (UDP套接字)

```python
Server:
    
	import socket
    ip_port=('127.0.0.1',8081)
    udp_server_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #买手机
    udp_server_sock.bind(ip_port)

    while True:
        qq_msg,addr=udp_server_sock.recvfrom(1024)
        print('来自[%s:%s]的一条消息:\033[1;44m%s\033[0m' %(addr[0],addr[1],qq_msg.decode('utf-8')))
        back_msg=input('回复消息: ').strip()

        udp_server_sock.sendto(back_msg.encode('utf-8'),addr)
```

```python
Client:
    
    import socket
    BUFSIZE=1024
    udp_client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    qq_name_dic={
        '狗哥alex':('127.0.0.1',8081),
        '瞎驴':('127.0.0.1',8081),
        '一棵树':('127.0.0.1',8081),
        '武大郎':('127.0.0.1',8081),
    }


    while True:
        qq_name=input('请选择聊天对象: ').strip()
        while True:
            msg=input('请输入消息,回车发送: ').strip()
            if msg == 'quit':break
            if not msg or not qq_name or qq_name not in qq_name_dic:continue
            udp_client_socket.sendto(msg.encode('utf-8'),qq_name_dic[qq_name])

            back_msg,addr=udp_client_socket.recvfrom(BUFSIZE)
            print('来自[%s:%s]的一条消息:\033[1;44m%s\033[0m' %(addr[0],addr[1],back_msg.decode('utf-8')))

    udp_client_socket.close()
```

### 时间服务器：

```python
Server:
    
	ip_port=('127.0.0.1',9000)
    bufsize=1024

    tcp_server=socket(AF_INET,SOCK_DGRAM)
    tcp_server.bind(ip_port)

    while True:
        msg,addr=tcp_server.recvfrom(bufsize)
        print('===>',msg)

        if not msg:
            time_fmt='%Y-%m-%d %X'
        else:
            time_fmt=msg.decode('utf-8')
        back_msg=strftime(time_fmt)

        tcp_server.sendto(back_msg.encode('utf-8'),addr)

    tcp_server.close()
```

```python
Client:
    
    from socket import *
    ip_port=('127.0.0.1',9000)
    bufsize=1024

    tcp_client=socket(AF_INET,SOCK_DGRAM)

    while True:
        msg=input('请输入时间格式(例%Y %m %d)>>: ').strip()
        tcp_client.sendto(msg.encode('utf-8'),ip_port)

        data=tcp_client.recv(bufsize)

        print(data.decode('utf-8'))

    tcp_client.close()
```

