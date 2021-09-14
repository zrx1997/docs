修改Linux网卡的驱动名称



### 1、修改网卡配置文件

```bash

cd /etc/sysconfig/network-scripts/
# 找到你想要修改的网卡的配置文件，修改NAME和DEVICE两个字段，修改为新的网卡名
NAME=xxx
DEVICE=xxx

改为
NAME=eth0
DEVICE=eth0


```



### 2、网卡配置文件重命名

```bash
# mv 旧网卡名	新网卡名
mv ifcfg-ens160 ifcfg-eth0

```



### 3、修改grub配置文件

```bash
vim /etc/sysconfig/grub

# 在GRUB_CMDLINE_LINUX末尾加入配置：net.ifnames=0 biosdevname=0
# 如下所示

GRUB_CMDLINE_LINUX="rd.lvm.lv=centos/root rd.lvm.lv=centos/swap crashkernel=auto rhgb quiet net.ifnames=0 biosdevname=0"

# 修改完成后使用以下命令重新生成grub配置并更新内核参数
grub2-mkconfig -o /boot/grub2/grub.cfg


```



### 4、添加udev的规则

```bash

在文件夹/etc/udev/rules.d中创建网卡规则文件：70-persistent-net.rules，并写入内容：

cd /etc/udev/rules.d

vim 70-persistent-net.rules

UBSYSTEM=="net",ACTION=="add",DRIVERS=="?",ATTR{address}=="00:0c:19:cd:62:38",ATTR｛type｝=="1" ,KERNEL=="eth",NAME="eth0"

网卡MAC地址00:0c:19:cd:62:38填写你的网卡MAC地址，是通过ip addr或ifconfig获取的。

然后重启即可
```



