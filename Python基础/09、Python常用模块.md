### 序列化模块-pickle

```python
dumps 把任意对象序列化成一个bytes
loads 把任意bytes反序列化成原来数据
dump  把对象序列化后写入到file-like Object(即文件对象)
load  把file-like Object(即文件对象)中的内容拿出来,反序列化成原来数据
```

### 数学模块-math

```python
ceil()  	向上取整操作 (对比内置round)
floor() 	向下取整操作 (对比内置round)
pow()  		计算一个数值的N次方(结果为浮点数) (对比内置pow)
sqrt() 		开平方运算(结果浮点数)
fabs() 		计算一个数值的绝对值 (结果浮点数) (对比内置abs)
modf() 		将一个数值拆分为整数和小数两部分组成元组
copysign()  将参数第二个数值的正负号拷贝给第一个 (返回一个小数)
fsum() 		将一个容器数据中的数据进行求和运算 (结果浮点数)(对比内置sum)
pi			圆周率常数
```

### 随机模块-random

```
random() 		获取随机0-1之间的小数(左闭右开)
randrange() 	随机获取指定范围内的整数(包含开始值,不包含结束值,间隔值)
randint()   	随机产生指定范围内的随机整数
uniform() 		获取指定范围内的随机小数(左闭右开)
choice()  		随机获取序列中的值(多选一)
sample()  		随机获取序列中的值(多选多) [返回列表]
shuffle() 		随机打乱序列中的值(直接打乱原序列)
```

### 时间模块-time

```
time()      获取本地时间戳
ctime()     获取本地时间字符串(参数是时间戳,默认当前)
localtime()     获取本地时间元组          (参数是时间戳,默认当前)
mktime()        通过时间元组获取时间戳    (参数是时间元组)
asctime()       通过时间元组获取时间字符串(参数是时间元组)
sleep()         程序睡眠等待
strftime()      格式化时间字符串(格式化字符串,时间元祖)
strptime()      将时间字符串通过指定格式提取到时间元组中(时间字符串,格式化字符串) 
perf_counter()  用于计算程序运行的时间

```

### 时间模块相关知识

```
#时间戳指从1970年1月1日0时0分0秒到指定时间之间的秒数,时间戳是秒,可以使用到2038年的某一天
#UTC时间: 世界约定的时间表示方式，世界统一时间格式，世界协调时间！
#夏令时:  在夏令时时间状态下，时间会调块1个小时

#时间元组是使用元祖格式表示时间的一种方式
    格式1(自定义):
        (年，月，日，时，分,秒，周几，一年中的第几天，是否是夏令时时间)
    格式2(系统提供):
        (tm_year = 年，tm_month = 月，tm_day = 日，tm _hour = 时， tm_min = 分, tm _sec = 秒， tm _wday = 周几， tm _yday = 一年中的第几天，tm_isdst = 是否是夏令时时间)

        0   年   4位数完整年份    四位数1997
        1   月   1-12月           1 - 12
        2   日   1-31天           1 - 31
        3   时   0-23时           0 - 23
        4   分   0-59分           0 - 59
        5   秒   0-61秒           0 - 61
        6   周几 周一-周天         0 - 6
        7   年中第几天    共366天  1 - 366
        8   夏令时  两种           0,1  0是  其他都不是  

#格式化时间字符串:
    格式    含义        
    %a    本地（locale）简化星期名称
    %A    本地完整星期名称
    %b    本地简化月份名称
    %B    本地完整月份名称
    %c    本地相应的日期和时间表示
    %d    一个月中的第几天（01 - 31）
    %H    一天中的第几个小时（24 小时制，00 - 23）
    %I    一天中的第几个小时（12 小时制，01 - 12）
    %j    一年中的第几天（001 - 366）
    %m    月份（01 - 12）
    %M    分钟数（00 - 59）
    %p    本地 am 或者 pm 的相应符    
    %S    秒（01 - 61）   
    %U    一年中的星期数（00 - 53 星期天是一个星期的开始）第一个星期天之前的所有天数都放在第 0 周    
    %w    一个星期中的第几天（0 - 6，0 是星期天）   
    %W    和 %U 基本相同，不同的是 %W 以星期一为一个星期的开始
    %X    本地相应时间
    %y    去掉世纪的年份(00 - 99)
    %Y    完整的年份
    %z    用 +HHMM 或 -HHMM 表示距离格林威治的时区偏移（H 代表十进制的小时数，M 代表十进制的分钟数）
    %%    %号本身
    
#--不常用的属性函数(了解)
    *gmtime()        获取UTC时间元祖(世界标准时间)
    *time.timezone   获取当前时区(时区的时间差)
    *time.altzone    获取当前时区(夏令时)
    *time.daylight   获取夏令时状态

```

### 日历模块-calendar(了解内容)

```
#--calendar 日历模块 import calendar
#calendar() 获取指定年份的日历字符串 (年份,w日期间的宽度,l日期间的高度,c月份间的间距,m一行显示几个月)
calendar.calendar(2018,w=2,l=2,c=20,m=1)

#month() 获取指定年月的日历字符串 (年份,月份,w日期之间的宽度,l日期之间的高度)
calendar.month(2018,9,w = 2,l = 2)

#monthcalendar() 获取指定年月的信息列表 (年份,月份) 0从周一开始排
calendar.monthcalendar(2018,9)

#isleap() 检测是否是润年(能被4整除不能被100整除或能被400整除)
calendar.isleap(2004)

#leapdays() 指定从某年到某年范围内的润年个数
calendar.leapdays(1970,2038)

#monthrange() 获取某年某月的信息 周一是0
calendar.monthrange(2018,8)

#weekday() 指定某年某月某日是星期几
calendar.weekday(2018,8,18)

#timegm() 将时间元组转化为时间戳
ttp = (2018,10,1,13,23,34,0,0,0)
calendar.timegm(ttp)
```

### os模块-对系统进行操作

```
#system()  在python中执行系统命令
#popen()   执行系统命令返回对象,通过read方法读出字符串
#listdir() 获取指定文件夹中所有内容的名称列表
#getcwd()  获取当前文件所在的默认路径
#chdir()   修改当前文件工作的默认路径
#environ   获取或修改环境变量
#--os 模块属性
#name 获取系统标识   linux,mac ->posix      windows -> nt
#sep 获取路径分割符号  linux,mac -> /       window-> \
#linesep 获取系统的换行符号  linux,mac -> \n    window->\r\n 或 \n
```

### os路径模块 -os.path

```
#basename() 返回文件名部分
#dirname()  返回路径部分
#split() 将路径拆分成单独的文件部分和路径部分 组合成一个元组
#join()  将多个路径和文件组成新的路径 可以自动通过不同的系统加不同的斜杠  linux / windows\
#splitext() 将路径分割为后缀和其他部分
#getsize()  获取文件的大小
#isdir()    检测路径是否是一个文件夹
#isfile()   检测路径是否是一个文件
#islink()   检测路径数否是一个链接
#getctime() [windows]文件的创建时间,[linux]权限的改动时间(返回时间戳)
#getmtime() 获取文件最后一次修改时间(返回时间戳)
#getatime() 获取文件最后一次访问时间(返回时间戳)
#exists()   检测指定的路径是否存在
#isabs()    检测一个路径是否是绝对路径
#abspath()  将相对路径转化为绝对路径
```

### os 与 shutil 模块 都具备对文件的操作

```
# -- os模块具有 新建/删除/
#os.mknod   创建文件
#os.remove  删除文件
#os.mkdir   创建目录(文件夹)
#os.rmdir   删除目录(文件夹)
#os.rename  对文件,目录重命名
#os.makedirs   递归创建文件夹
#os.removedirs 递归删除文件夹（空文件夹）
```

### shutil模块

```
# -- shutil模块 复制/移动/
#copyfileobj(fsrc, fdst[, length=16*1024])  复制文件 (length的单位是字符(表达一次读多少字符))
#copyfile(src,dst)   #单纯的仅复制文件内容 , 底层调用了 copyfileobj
#copymode(src,dst)   #单纯的仅复制文件权限 , 不包括内容  (虚拟机共享目录都是默认777)
#copystat(src,dst)   #复制所有状态信息,包括权限，组，用户，修改时间等,不包括内容
#copy(src,dst)       #复制文件权限和内容
#copy2(src,dst)      #复制文件权限和内容,还包括权限，组，用户，时间等
#copytree(src,dst)   #拷贝文件夹里所有内容(递归拷贝)
#rmtree(path)        #删除当前文件夹及其中所有内容(递归删除)
#move(path1,paht2)   #移动文件或者文件夹
```

### json模块

```
# 所有编程语言都能够识别的数据格式叫做json,是字符串
#dumps 把任意对象序列化成一个str
#loads 把任意str反序列化成原来数据
#dump  把对象序列化后写入到file-like Object(即文件对象)
#load  把file-like Object(即文件对象)中的内容拿出来,反序列化成原来数据

# json 和 pickle 两个模块的区别:
(1)json序列化之后的数据类型是str,所有编程语言都识别,
   但是仅限于(int float bool)(str list tuple dict None)
   json不能连续load,只能一次性拿出所有数据
(2)pickle序列化之后的数据类型是bytes,
   所有数据类型都可转化,但仅限于python之间的存储传输.
   pickle可以连续load,多套数据放到同一个文件中
```

### 压缩模块-zipfile (后缀为zip)

```
#zipfile.ZipFile(file[, mode[, compression[, allowZip64]]])
#ZipFile(路径包名,模式,压缩or打包,可选allowZip64)
#功能：创建一个ZipFile对象,表示一个zip文件.
#参数：
    -参数file表示文件的路径或类文件对象(file-like object)
    -参数mode指示打开zip文件的模式，默认值为r
        r    表示读取已经存在的zip文件
        w    表示新建一个zip文档或覆盖一个已经存在的zip文档
        a    表示将数据追加到一个现存的zip文档中。
    -参数compression表示在写zip文档时使用的压缩方法
        zipfile.ZIP_STORED      只是存储模式，不会对文件进行压缩，这个是默认值
        zipfile.ZIP_DEFLATED    对文件进行压缩 
    -如果要操作的zip文件大小超过2G，应该将allowZip64设置为True。

#压缩文件
#1.ZipFile()          写模式w打开或者新建压缩文件
#2.write(路径,别名)   向压缩文件中添加文件内容
#3.close()            关闭压缩文件

#解压文件
#1.ZipFile()             读模式r打开压缩文件
#2.extractall(路径)      解压所有文件到某个路径下
#  extract(文件,路径)    解压指定的某个文件到某个路径下
#3.close()               关闭压缩文件

#追加文件(支持with写法)
ZipFile()                追加模式a打开压缩文件

#查看压缩包中的内容
namelist()
```

### 压缩模块-tarfile(后缀为.tar  |  .tar.gz  |   .tar.bz2)

```
#bz2模式的压缩文件较小  根据电脑的不同会差生不同的结果 (理论上:bz2压缩之后更小,按实际情况为标准)

w     单纯的套一个后缀 打包
w:bz2 采用bz2算法 压缩    
w:gz  采用gz算法 压缩

#压缩文件
#1.open('路径包名','模式','字符编码') 创建或者打开文件 
#2.add(路径文件,arcname="别名") 向压缩文件中添加文件
#3,close() 关闭文件

#解压文件
#1.open('路径包名','模式','字符编码') 读模式打开文件 
#2.extractall(路径)      解压所有文件到某个路径下
#  extract(文件,路径)    解压指定的某个文件到某个路径下
#3.close()               关闭压缩文件

#追加文件
open()                   追加模式 a: 打开压缩文件 正常添加即可

#查看压缩包中的内容
getnames()    
```



### sys模块

```python

```



### 日志模块

```python
import logging  # 引入logging模块
# 将信息打印到控制台上
logging.debug(u"苍井空")
logging.info(u"麻生希")
logging.warning(u"小泽玛利亚")
logging.error(u"桃谷绘里香")
logging.critical(u"泷泽萝拉")
```



### filecmp

```
文件及目录比较模块
	https://docs.python.org/zh-cn/3.6/library/filecmp.html

文件差异比较
	https://docs.python.org/zh-cn/3/library/difflib.html
```

### psutil

```
系统进程相关
```

