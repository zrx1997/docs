文件处理

```python
什么是文件：
	应用程序若想操作硬件必须通过操作系统，而文件就是操作系统提供给应用程序来操作硬盘的虚拟概念，用户或应用程序对文件的操作，就是向操作系统发起调用，然后由操作系统完成对硬盘的具体操作。
    
为什么要用文件：
	应用程序运行的过程中产生的数据最先都是存放于内存中的，若想永久保存下来，必须要保存在硬盘中。
    
文件的操作流程：
		1、打开文件，由应用程序向操作系统发起系统调用open(...)，操作系统打开该文件，对应一块硬盘空间，并返回一个文件对象赋值给一个变量f
		2、调用文件对象下的读/写方法，会被操作系统转换为读/写硬盘的操作
		3、向操作系统发起关闭文件的请求，回收系统资源
			f = open('a.txt','r',encoding='utf-8')      
            		#1.文件名，可以是绝对路径，2.文件的模式，3.指定字符编码
			data = f.read()    
            		#调用文件对象下的读/写方法，然后赋值给data
			print(data)
			f.close()          #通知操作系统关闭文件，回收资源
            

```

文件的操作模式

```python
文件的操作模式：
	r(默认的)：只读
	w：只写
	a：只追加写
    x：xor异或模式()
    
r模式的使用：
    r只读模式：在文件不存在时则报错,文件存在文件内指针直接跳到文件开头
        with open('a.txt',mode='r',encoding='utf-8') as f:
            res=f.read() # 会将文件的内容由硬盘全部读入内存，赋值给res
			
    w模式的使用：
        w只写模式：在文件不存在时会创建空文档,文件存在会清空文件,文件指针跑到文件开头
            with open(r'C:\Users\windows\Desktop\db.txt',mode='w',encoding='utf-8') as f:
                f.write('admin\n')
                f.write('passwd')
        注：
            在文件不关闭的情况下,连续的写入，后写的内容一定跟在前写内容的后面
            如果重新以w模式打开文件，则会清空文件内容
		
    a模式的使用：
        a只写追加模式：在文件不存在时会创建空文档,文件存在会将文件指针直接移动到文件末尾
            with open(r'C:\Users\windows\Desktop\db.txt',mode='a',encoding='utf-8') as f:
                f.write('11111\n')
                f.write('22222')
        w模式与a模式的对比：
            相同点：在打开的文件不关闭的情况下，连续的写入，新写的内容总会跟在前写的内容之后
            不同点：以 a 模式重新打开文件，不会清空原文件内容，会将文件指针直接移动到文件末尾，新写的内容永远写在最后
            
    +模式的使用（了解）：
        r+ w+ a+ :可读可写
    在平时工作中，我们只单纯使用r/w/a，要么只读，要么只写，一般不用可读可写的模式
     
```

with机制

```python
资源回收与with上下文管理：
    打开一个文件包含两部分资源：
        应用程序变量
        操作系统打开的文件
    在操作完毕一个文件的时候，必须把与该文件的这两部分资源全部收回
        回收操作系统打开的文件资源
        回收应用程序级的变量
    其中，回收应用程序级别的变量必须在回收操作系统资源之后，但是python自带的垃圾回收机制决定了我们无需考虑回收应用程序变量，因此我们只需要记住回收操作系统资源就可以了
    
with机制：
    有时候，我们可能会忘记回收操作系统打开的文件资源，因此Python提供了一种机制来帮我们解决这个问题
    with open('a.txt','r',encoding='utf-8') as f:    
        	#在执行完子代码块后，with 会自动执行f.close()
        data = f.read()
        print(data)

    with open('a.txt', 'r') as read_f, open('b.txt', 'w') as write_f:      
        	# 可用用with同时打开多个文件，用逗号分隔开即可
        data = read_f.read()
        write_f.write('data')             #括号内是写入的内容

    f = open(...)是由操作系统打开文件，如果打开的是文本文件，会涉及到字符编码问题，如果没有为open指定编码，那么打开文本文件的默认编码很明显是操作系统说了算了，操作系统会用自己的默认编码去打开文件，在windows下是gbk，在linux下是utf-8。若要保证不乱码，文件以什么方式存的，就要以什么方式打开，encoding='utf-8'指定字符编码

```

文件读写内容的模式

```python
控制文件读写内容的模式：
    t：文本模式（默认的）
        读写文件都是以字符串为单位的
        只能针对文本文件
        必须指定encoding参数
    b：二进制模式:
        读写文件都是以bytes/二进制为单位的
        可以针对所有文件
         一定不能指定encoding参数
    注：tb模式均不能单独使用，必须与r/w/a之一结合使用
		
t模式的使用：
    t 模式：如果我们指定的文件打开模式为r/w/a，其实默认就是rt/wt/at
    t 模式只能用于操作文本文件,无论读写，都应该以字符串为单位，而存取硬盘本质都是二进制的形式，当指定 t模式时，内部帮我们做了编码与解码。

         with open('a.txt',mode='rt',encoding='utf-8') as f:
             res=f.read() 
             print(type(res)) # 输出结果为：<class 'str'>

         with open('a.txt',mode='wt',encoding='utf-8') as f:
             s='abc'
             f.write(s) # 写入的也必须是字符串类型
				
b模式的使用：
    b: 读写都是以二进制位单位
         with open('1.mp4',mode='rb') as f:
             data=f.read()
             print(type(data)) # 输出结果为：<class 'bytes'>

         with open('a.txt',mode='wb') as f:
             msg="你好"
             res=msg.encode('utf-8') # res为bytes类型
             f.write(res) # 在b模式下写入文件的只能是bytes类型

    b模式对比t模式
        1、在操作纯文本文件方面t模式帮我们省去了编码与解码的环节，b模式则需要手动编码与解码，所以此时t模式更为方便
        2、针对非文本文件（如图片、视频、音频等）只能使用b模式
        
案例：编写拷贝工具
    src_file=input('源文件路径: ').strip()
    dst_file=input('目标文件路径: ').strip()
    with open(r'%s' %src_file,mode='rb') as read_f,open(r'%s'%dst_file,mode='wb') as write_f:
        for line in read_f:
            # print(line)
        write_f.write(line)
```

操作文件的方式

```python
读操作：
    f.read()          # 读取所有内容,执行完该操作后，文件指针会移动到文件末尾
    f.readline()      # 读取一行内容,光标移动到第二行首部
    f.readlines()     # 读取每一行内容,存放于列表中
	注：f.read()与f.readlines()都是将内容一次性读入内容，如果内容过大会导致内存溢出，若还想将内容全读入内存，则必须分多次读入，有两种实现方式：
    方式一：
        with open('a.txt',mode='rt',encoding='utf-8') as f:
            for line in f:
                print(line)              # 同一时刻只读入一行内容到内存中
    方式二：
        with open('1.mp4',mode='rb') as f:
            while True:
                data=f.read(1024) # 同一时刻只读入1024个Bytes到内存中
                if len(data) == 0:
                    break
                print(data)
                
                
写操作：
    f.write('1111\n222\n')                    # 针对文本模式的写,需要自己写换行符
    f.write('1111\n222\n'.encode('utf-8'))    # 针对b模式的写,需要自己写换行符
    f.writelines(['333\n','444\n'])           # 文件模式
    f.writelines([bytes('333\n',encoding='utf-8'),'444\n'.encode('utf-8')])   #b模式
	# f.writeline 将内容是字符串的可迭代性数据写入文件中 参数:内容为字符串类型的可迭代数据
了解：
    f.readable()  # 文件是否可读
    f.writable()  # 文件是否可写
    f.closed  # 文件是否关闭
    f.encoding  # 如果文件打开模式为b,则没有该属性
    f.flush()  # 立刻将文件内容从内存刷到硬盘
    f.name
	f.truncate() # 把要截取的字符串提取出来,然后清空内容将提取的字符串重新写入文件中 (字节)
    
    encode() 编码  将字符串转化为字节流(Bytes流)
    decode() 解码  将Bytes流转化为字符串
```

控制文件指针的移动

```python
文件内指针的移动都是Bytes为单位的,唯一例外的是t模式下的read(n),n以字符为单位
    with open('a.txt',mode='rt',encoding='utf-8') as f:
         data=f.read(3)       # 读取3个字符

    with open('a.txt',mode='rb') as f:
         data=f.read(3)       # 读取3个Bytes

之前文件内指针的移动都是由读/写操作而被动触发的，若想读取文件某一特定位置的数据，则需要用f.seek方法主动控制文件内指针的移动，详细用法如下：
    f.seek(指针移动的字节数,模式控制): 
        模式控制:
            0: 默认的模式,该模式代表指针移动的字节数是以文件开头为参照的
            1: 该模式代表指针移动的字节数是以当前所在的位置为参照的
            2: 该模式代表指针移动的字节数是以文件末尾的位置为参照的
            强调：其中0模式可以在t或者b模式使用,而1跟2模式只能在b模式下用

    0模式：
         a.txt用·个字节，中文“你好”各占3个字节）
         abc你好

        # 0模式的使用
        with open('a.txt',mode='rt',encoding='utf-8') as f:
            f.seek(3,0)     # 参照文件开头移动了3个字节
            print(f.tell()) # 查看当前文件指针距离文件开头的位置，输出结果为3
            print(f.read()) # 从第3个字节的位置读到文件末尾，输出结果为：你好
            # 注意：由于在t模式下，会将读取的内容自动解码，所以必须保证读取的内容是一个完整中文数据，否则解码失败

        with open('a.txt',mode='rb') as f:
            f.seek 	(6,0)
            print(f.read().decode('utf-8')) #输出结果为: 好

    1模式：
        # 1模式的使用
        with open('a.txt',mode='rb') as f:
            f.seek(3,1) # 从当前位置往后移动3个字节，而此时的当前位置就是文件开头
            print(f.tell()) # 输出结果为：3
            f.seek(4,1)     # 从当前位置往后移动4个字节，而此时的当前位置为3
            print(f.tell()) # 输出结果为：7

    2模式：
        # a.txt用utf-8编码，内容如下（abc各占1个字节，中文“你好”各占3个字节）
        abc你好

        # 2模式的使用
        with open('a.txt',mode='rb') as f:
            f.seek(0,2)     # 参照文件末尾移动0个字节， 即直接跳到文件末尾
            print(f.tell()) # 输出结果为：9
            f.seek(-3,2)     # 参照文件末尾往前移动了3个字节
            print(f.read().decode('utf-8')) # 输出结果为：好
            
    read()	读取字符的个数(里面的参数代表字符个数)
    seek()	调整指针的位置(里面的参数代表字节个数)
    tell()	当前光标左侧所有的字节数(返回字节数)
    
刷新缓冲区flush
    当文件关闭的时候自动刷新缓冲区
    当整个程序运行结束的时候自动刷新缓冲区
    当缓冲区写满了  会自动刷新缓冲区
    手动刷新缓冲区
    
#小练习：实现动态查看最新一条日志的效果
import time
with open('access.log',mode='rb') as f:
    f.seek(0,2)
    while True:
        line=f.readline()
        if len(line) == 0:
            # 没有内容
            time.sleep(0.5)
        else:
            print(line.decode('utf-8'),end='')

```

文件的修改

```python
文件a.txt内容如下：
    张一蛋     山东    179    49    12344234523
    李二蛋     河北    163    57    13913453521
    王全蛋     山西    153    62    18651433422

执行操作：
    with open('a.txt',mode='r+t',encoding='utf-8') as f:
        f.seek(9)
        f.write('<妇女主任>')

文件修改后的内容如下
    张一蛋<妇女主任> 179    49    12344234523
    李二蛋     河北    163    57    13913453521
    王全蛋     山西    153    62    18651433422

强调：
    1、硬盘空间是无法修改的,硬盘中数据的更新都是用新内容覆盖旧内容
    2、内存中的数据是可以修改的
注：
    文件对应的是硬盘空间,硬盘不能修改对应着文件本质也不能修改，我们看到的文件的修改大致的思路是将硬盘中文件内容读入内存,然后在内存中修改完毕后再覆盖回硬盘
文件修改的两种方式：
    方式一：
        实现思路：将文件内容发一次性全部读入内存,然后在内存中修改完毕后再覆盖写回原文件
        优点: 在文件修改过程中同一份数据只有一份
        缺点: 会过多地占用内存

        with open('db.txt',mode='rt',encoding='utf-8') as f:
            data=f.read()

        with open('db.txt',mode='wt',encoding='utf-8') as f:
            f.write(data.replace('kevin','SB'))

    方式二：
        实现思路：以读的方式打开原文件,以写的方式打开一个临时文件,一行行读取原文件内容,修改完后写入临时文件...,删掉原文件,将临时文件重命名原文件名

        优点: 不会占用过多的内存
        缺点: 在文件修改过程中同一份数据存了两份

        import os

        with open('db.txt',mode='rt',encoding='utf-8') as read_f,\
                open('.db.txt.swap',mode='wt',encoding='utf-8') as wrife_f:
            for line in read_f:
                wrife_f.write(line.replace('SB','kevin'))

        os.remove('db.txt')
        os.rename('.db.txt.swap','db.txt')


```

