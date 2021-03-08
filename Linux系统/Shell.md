# 知识概述

### 基础知识部分：

- 变量知识概念
- 脚本执行方法
- 系统正则知识

### 进阶知识部分

- 脚本算法知识
- 脚本信息比较
- 判断语句if case
- 循环语句for while until

### 高级知识部分

- 脚本函数概念
- 脚本数组概念

# Shell脚本基础介绍

### 学习Shell目的

- 提高工作效率
- 减少重复工作
- 完成批量操作
- 节省人力成本

### 学习Shell方法

- 掌握系统的基础命令
- 掌握系统正则符号
- 掌握脚本语句用法

> 混合在一起用的时候，是否复合逻辑

### 变量知识概念

##### 1.常规变量：

临时变量：在脚本中或命令行中设置，    oldboy = 123

永久变量：在特殊的系统变量文件中设置， 比如以下文件里：

```bash
etc/profile
etc/bashrc
~/.bashrc
~/.bash_profile
```

设置变量：

1）进行字符串设置：

```shell
name="oldboy" 
name="123456" 
name="oldboy edu python"
```

2）进行变量调用

```shell
info="python"
name="$info"  # 调用name=info变量
```

3）进行命令信息设置：比如在不同的主机上创建一个文件夹，文件夹的名字以ip命名，名字是IP_info

```shell
IP_info="$(hostname -i)"
IP_info=`hostname -i`
```

##### 2.环境变量:

有export定义变量：对当前登陆窗口所有shell都生效

无export定义变量，只对当前的shell生效

```shell
export INFO="XXXX"
```



###### 变量赋值方式

①变量赋值： 

```
a=1 
b=2 
echo $a $b
```

​    service  启动或重启或停止服务

②传参赋值：a=$1 b=$2

```shell
a=$1
b=$2
./test.sh      # 执行文件
./test.sh oldboy oldgirl    # 这就是把oldboy赋值成a, 把oldgirl赋值成b
```



③交互赋值：需要交互询问信息进行赋值

```shell
read -p "请输入学员姓名：" name age
echo $name >> class.txt  # >> 表示追加到文件中
echo $age >> class.txt
```



##### 3.特殊变量

```shell
$0:	用于获取脚本名称信息，直接显示脚本名称和路径信息
	echo "$0脚本执行失败，请检查脚本逻辑"
	
$#：统计出脚本的传入参数总数

$*：输出脚本所有参数信息

$@：输出脚本所有参数信息

$?：输出命令执行返回值  利用返回值可以判断命令是否执行成功
    0 		表示操作执行成功
	非0		表示操作执行失败

$$  获取一个脚本执行PID信息

$!  获取上一个程序或脚本后台运行pid信息
    sh test.sh &    --- 让脚本后台运行

$_  获取脚本的最后一个参数信息
    sh test.sh  a b c 
	echo $_
	c 
```



--------------------------------------------------------------------------------------------------------------

### 脚本执行方法

① 直接授权脚本执行权限，直接运行脚本

```shell
./test.sh
/root/test.sh
```

②利用命令信息执行脚本

 利用命令解释器执行脚本

```shell
sh ./test.sh bash ./test.sh    
```

脚本之间信息加载调用

```shell
source ./test.sh
```

### 系统正则知识

可以用到正则的命令，可以直接加载基本正则

> grep：过滤
>
> sed：编辑
> awk：文件的分析处理



> 帮助：man gerp/sed/awk

基础正则符号：^ $ ^$ . `*` .* \ [] [^]

```
^ : 可以匹配以指定信息开头的内容
	eg：grep ^o test.txt

$ : 可以指定以什么结尾的内容

^$ : 可以匹配空行信息
	eg：grep ^$ test.txt
	    grep -v ^$ test.txt  # 不显示空行 
		grep -vE "^$|^#" test.txt  #  排除注释（以#开头）和空行信息

. : 匹配任意且只有一个字符信息

* : 匹配任意一个字符连续出现0次或多次的情况
	eg: gd god good goood gooood gad gbd gcd
	过滤：grep g.o test.txt   显示： god gad gbd gcd
	过滤：grep go*d test.txt  显示： gd god good goood gooood
	过滤：grep ^g.*d$ test.txt  显示： 所有的

.* : 匹配任意所有任容（包括无内容）
	
\ : 转义符号 （有意义的信息变得无意义）（将没有意义的信息变得有特殊意义）
	用法：在符号前面加一个撬棍(grep \.d$ test.txt)

[] : 批量取出多个字符信息
	eg：比如拿出所有的大写字母
	grep "[A-Z]" test.txt  # 把所有带有大写字母的行，都过滤出来

[^] : 排除指定的多个字符信息进行过滤
	eg: 排除数字为4， 7的车牌子
	grep "[^4]" test.txt

```



扩展正则符号：+ | {} () ?

> grep 需要加 -E 才可以用扩展正则    eg： grep -E 过滤
>
> sed 需要加-r  才可以用扩展正则       eg: sed -r 编辑

文件

```
gd
god
good 
goood
gooood
```

方法

```shell
+ : 匹配任意一个字符连续出现1次或多次情况
	eg: grep -E "o+" test.txt   显示：god good goood gooood
	
| : 可匹配多个信息，多个信息之间存在或者关系

{} : 可以指定连续匹配的次数信息
	{n}： 正好连续n次
	{n，}： 最少连续出现n次，超过n次默认也匹配（默认贪婪）
	{，n}： 最多连续出现n次，少于n次默认也匹配
	{n，m}： 最少连续出现n次，最多连续出现m次
	eg: grep -E "o{3,}" test.txt  显示：少于三个o的信息： god good goood gooood  因为贪婪模式，所以有gooood
		grop -E "o{3}" test.txt  显示： goood gooood 默认贪婪模式
		
() : 将多个字符信息当作一个整体匹配
	eg：grep -E "(god)" test.txt
	
? : 匹配任意一个字符信息连续出现0次或者1次的情况
	eg：grep E "go?d" test.txt
	
```



# 进阶知识部分

### 基本算法知识

① $(()) : 实现数值信息运算（只支持整数运算，加减乘除）

```shell
echo $((1+2))
>>> 3
echo $((2-1))
>>> 1
```

②$((a++)) : 自增自减运算（只支持整数）

```shell
echo $((10--))
>>> 10
echo $((10--))
>>> 9
```

立刻马上做自增运算

```shell
echo $((++10))
>>> 11
```

③let ： 实现数值信息运算（只支持整数）

```shell
i=1
let i=i+8
echo $i
>>> 10
```



运算的应用：

企业案例:监控web页面状态信息，失败2次，就实现报警功能

```
!/bin/bash
timeout = 5  # 延迟时间
fails = 0  # 失败次数
success = 0  # 成功次数
url = $1  # url

while ture
do
	wget -- timeout=$timeout -- tries=1 http://$uel -q
	if [ $? -ne 0 ]
	then
		let fails=fails+1
	else
		ler seccess++
	fi
	
	if [ $fails -eq 2 ]
	then
		mail 报警信息 谁谁谁
	fi
done
```

最后输入命令，在后台监控

```
sh jiankong.sh http://www.baidu.com $
```



> 
>
> wget：最简单的爬虫的命令，比如下载一个不能进行复制操作的页面。
>
> tries：可以尝试的次数，如果超过，就报错
>
> q: 安静的执行



④expr : 实现数据信息的运算（只支持整数运算）

```shell
rpm -qf `whick expr`  # 下载

expr 1 + 1
>>> 2
expr 2 - 1
>>> 1

i = 4
expr $i - 2
>>> 2
```

expr 还可以做整数判断

```shell
a=$1
expr $a + 0 $>/dev/null
[ $? -eq 0 ] $$ echo 输入的信息是整数 || echo 输入的是非整数
```

> || 否则的意思
>
> 输入相应类型的数字，会输出echo后面的文字



⑤bc ： 实现数值信息运算，支持整数和小数

```shell
echo 3+5|bc
>>> 8
echo 3.1 + 5.6 | bc
>>> 8.7
```



### 脚本信息比较

①数值信息比较：

eg：记录学员信息，如果学员年龄信息大于30岁，不能进行录取

```shell
#!/bin/bash

read -p "请问你年龄多少：" age
if [ $age -gt 30 ]
then
	不能进行录取
else
	欢迎加入大家庭
fi
```

> -gt ： 大于
>
> -lt ：小于
>
> -eq： 等于
>
> -ne ： 不等于
>
> -le ： 小于等于
>
> -ge :  大于等于

执行脚本

```
sh test.sh
```



②字符信息比较：

eg：验证员工口令，口令通过可以进入公司

```shell
#!/bin/bash

read -p "请说出口令信息：" string
if [ $string == "天王盖地虎" ]
then
	进来吧，宝贝
else
	玩蛋去吧，宝贝
fi
```

> == ： 表示字符信息匹配成功
>
> != ： 表示匹配失败，不等于

执行脚本

```
sh test.sh
```





### 判断语句说明

##### if判断语句

1）单分支判断语句

> 如果....就....

```shell
if [好看]
then
	和他嘿嘿嘿
fi
```

2）双分支判断语句

> 如果....就....否则

```shell
if [好看]
then
	和他/她在一起
else
	培养培养
fi
```



3）多分支判断语句

> 如果...再如果...否则...

```shell
if [好看]
then
	在一起
elif [身材好]
then
	在一起
elif [有钱]
then
	在一起
else
	拉倒吧
fi
```



eg01: 输入两个数字，判断两个数字是否是整数

> 只要文件里面首行有   `#!/bin/bash`那么就是shell脚本

```
#!/bin/bash
read -p "请输入第一个数字：" num1
read -p "请输入第二个数字：" num2
if [ -z "$num1" ]
then
	echo "输入的第一个数字为空， 请重新输入"
	exit
elif [ -z "$num2" ]
then
	echo "输入的第二个数字为空，请重新输入"
	exit
elif [[ "$num1" =~ ^[0-9]+$ && "$num2" =~ ^[0-9]+$ ]]
then
	echo "对的，全是整数"
else
	echo "输入的数字非整数"
	exit
fi
```

> -z ： 代表是否为空zero
>
> exit：中断脚本，并从新输入
>
> =~ ： 数值是否与正则信息匹配
>
> && : and
>
> || : or



eg02：判断当前网络地址中，有哪些地址是已使用地址，有哪些地址是未使用地址

> 用ping来测试
>
> -c   ：
>
> -W：只测3秒
>
> &>/dev/null : 不看连接的信息

```shell
#!/bin/bash
for ip in 10.0.0.{1..254}
do
	ping -c 3 -W 3 $ip &>/dev/null
	if [ $? -eq 0 ]
	then
		echo $ip is online
	else
		echo $ip is offline
	fi
done
```

> ps -ef |grep sh：查看脚本进程
>
> kill 进程号

并行脚本  {}&

```
#!/bin/bash
for ip in 10.0.0.{1..254}
do
	{ ping -c 3 -W 3 $ip &>/dev/null
	if [ $? -eq 0 ]
	then
		echo $ip is online
	else
		echo $ip is offline
	fi } &
done
```



eg03：猜商品价格(1-100里面猜)，已知鼠标=随机生成一个小于100的正整数

知识：如何生成随机数字：

方法一：通过random变量产生随机数

```shell
echo $RANDOM 
```

> 范围 0-32768

方法二：通过openssl生成随机字符

```shell
openssl rand -bash64 10
```



![1597387452544](C:\Users\86188\AppData\Roaming\Typora\typora-user-images\1597387452544.png)

方法三：通过时间信息获取随机数

```shell
date +%S%N
```

方法四：利用UUID文件生成随机数

```shell
cat /proc/sys/kernel/random/uuid
```



猜数字脚本：

```shell
#!/bin/bash
num=`echo $((RANDOM%100+1))`
echo $num >/tmp/oldbot.txt

while true
do
	let i++
	read -p "请输入一个数字[1-100]:" info
	if [ $info -gt $num ]
	then
		echo "你输入的数字大了"
	elif [ $info -lt $num ]
	then
		echo "你输入的数字小了"
	else
		echo "你猜对了 总共猜了 $i 次"
		exit
	fi
done
```

> % ：取模运算，取余数 RANDOM%100 范围为0-99
>
> +1： 1-100的范围



##### case判断语句：

流程控制语句 == 多分支语句

语句格式：

```shell
case 变量名 in
	模式匹配1）
		模式1匹配处理
		;;
	模式匹配2）
		模式2匹配处理
		;;
	模式匹配3）
		模式3匹配处理
		;;
	*）
		其他模式匹配处理
esac
```



eg01：根据学习的课程显示报价：

```shell
#!/bin/bash
echo -e "魔兽世界人物\n伊利丹\n瓦里安\n女王"
read -p "请选择你要选择的任务， 可以提供人物技能参考：" name

case $name in
illidan|ILLIDAN)
	echo illidan 恶魔猎手 闪避
	;;
varuan|VARUAN)
	echo varuan 圣战士 雷霆之锤
	;;
queen|QUEEN)
	echo queen 游侠 沉默
	;;
	*)
	echo 没这人
esac

```



eg02：菜单功能进行自动化管理

```shell
#!/bin/bash
cat <<EOF
1.显示系统负载信息
2.显示系统磁盘信息
3.显示系统内存信息
4.显示系统登陆用户
EOF

while true
do
read -p "请输入想要查看的系统信息编号：" num 
case $num in
1)
	uptime
	;;
2)
	df -h
	;;
3)
	free -h
	;;
4)
	w
	;;
*)
	echo "请输入选项编号："
esac
done

```



### 循环语句

> for   while   until

##### for循环：有限循环

```
for 变量名称 in 循环范围 {1..10} /oldboy oldgirl / oldboy{1..10} / `cat user_list.txt`
do
	循环操作命令
done
```



EG：

```shell
#!/bin/bash
for user in oldman{1..10}
do
	useradd $user
done
```



##### while循环：无限循环（守护进程）

当设置为有限循环时，只有条件不满足时，循环结束

```
while 条件=true  循环就会一直执行
while 条件=false 循环就会立刻终止
```



无限循环：

```
while true
do
	每次循环做的操作
done
```



有限循环：

```shell
while [ 条件表达式 ]
do
	循环做的事
done
```



EG：

```shell
while [ $i -le 10 ]
do
	echo oldboy $i
	let i++
done
```





##### until循环：无限循环（守护进程）

当设置为有限循环时，只有条件满足时，循环结束

```shell
until 条件=true  循环就会立刻终止
until 条件=false 循环就会一直执行
```



无限循环：

```
until false
do
	每次循环做的操作
done
```



有限循环：

```shell
while [ 条件表达式 ]
do
	循环做的事
done
```



# 高级知识部分

### 脚本函数概念

概念：命令的集合，完成特定功能代码块，代码块可以实现复用



```shell
函数名称() {
    [ $# -ne 2 ] && echo 输入两个参数
}
```



函数的定义方法：

第一种

```
test1(){
    echo `定义个函数`
}
```



第二种

```
funcation test1(){
    echo `定义一个函数`
}
```



第三种

```shell
function test3{
    echo `定义一个函数`
}
```



使用

```shell
test1
test2
test3
```



### 脚本数组概念

将大量不同元素进行整合汇总，汇总信息称为数组

```shell
array[xx]=(oldboy oldgirl oldman)
```



设置一个数组

```shell
array=(oldboy oldgirl oldman)
```

调用数组指定元素值

```
echo ${array[1]}
>>> oldboy
echo ${array[2]}
>>> oldgirl
echo ${array[3]}
>>> oldman
```

调用数组整体 `*`

```shell
echo ${array[*]}
```

查看数组元素的数量 `#`

```shell
echo ${#array[*]}
```



EG:给班级学员进行学号设置：

```shell
#!/bin/bash
array=(
oldboy
oldgirl
oldman
alex
tank
)

for ((i=0;i<${#array[*]};i++))
do
	echo "我是第$i学号学员，我的姓名是$[arrat[$i]],哈哈哈"
done
```



> 资料：百度搜索shell脚本100道练习题