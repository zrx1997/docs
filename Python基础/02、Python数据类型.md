# 字符串

### 一、 字符串的定义

```python
1.1 字符串的定义

int()可以将由纯整数构成的字符串直接转换成整型，若包含其他任意非整数符号，则会报错
float()用来将字符串类型的小数转换成浮点型
	在单引号\双引号\三引号内包含一串字符
    text1 = 'aaa'
    text2 = "bbb"
    text3 = """cccc"""
1.2 字符串的拼接
	两个字符串类型可以拼接在一起
	a = "hello" + "word"
1.3 字符串的重复
	a = "python开发" * 3 #python开发python开发python开发
    
1.4 字符串的跨行拼接
	\
    a = "abc" \
    "def"
    等同于 a = "abcdef"
    
1.5 字符串的索引
	正向索引：同列表取值
    逆向索引：从右边开始，-1
    
1.6 索引的切片：
	[开始索引]：从开始索引截取到字符串的最后
    	strvar = "abcdef"
        strvar[3:]	# "def"
	[结束索引]： 从开头语截取到结束索引之前（结束索引-1）
    	strvar[:3]  # "abc"
    [开始索引：结束索引]：从开始索引截取到结束索引之前（结束索引-1）
    	strvar[0:3]  # "abc"
    [开始索引:结束索引:间隔值]：从开始索引截取到结束索引之前按照指定的间隔截取字符
    	strvar[0:6:2] # "ace"
    	strvar[::-1]  # "fedcba" 倒序
	[:]或[::]：截取所有字符串
    	strvar[::]  # "abcdef"
```

### 二、字符串的内置方法

```python
capitalize：字符串首字母大写
	strvar = "abcdef"
	print(strvar.capitalize())   # Abcdef

title：每个单词的首字母大写
	strvar = "hello word"
	print(strvar.title())		# Hello Word
    
upper：将字符串中所有的字母变成大写
	strvar = "adcwb"
	print(strvar.upper()) 		# ADCWB
    
lower：将字符串中所有的字母变成小写
	starvar = "ADCWB"
    print(strvar.lower()) 		# adcwb

swapcase：大小写互换
    strvar = "Hello Word"
	print(strvar.swapcase()) 	#hELLO wORD

len： 计算字符串长度
	strvar = "adcwb"
    print(len(strvar))			# 5
    
count：统计字符串中某个元素的数量
	strvar = "abcaab"
    print(strvar.count("a"))	# 3
 
find：查找某个字符串第一次出现的索引位置
	strvar = "adcwb"
    print(strvar.find("b"))		# 4
    字符串.find("字符",开始索引,结束索引) 如果找不到直接返回-1
    
index：等同于find
	index在找不到值的时候，会抛出异常，find在找不到的时候返回-1
    
startswith：判断是否以某个字符或字符串开头
	strvar = "adcwb"
    print(strvar.startswith("a"))   #返回布尔值
    字符串.startswith("字符",开始索引,结束索引) 如果存在返回True,否则返回False
  
endswith：判断是否以某个字符或字符串结尾
	strvar = "adcwb"
    print(strvar.endswith("b"))		#返回布尔值
    
isupper：判断字符串是否全部都是大写字母
	stavar = "ABCDEF"
    print(strvar.isupper())		#返回布尔值
    
islower：判断字符串是否全部都是小写字母
	stavar = "adcdef"
    print(strvar.islower())			# 返回布尔值
    
isdecimal：判断字符串是否是纯数字组成
	strvar = "123456"
    print(strvar.isdecimal())			# 返回布尔值
    
center,ljust,rjust,zfill ：控制输出格式
	center：填充字符串，原字符串居中显示，默认填充空格
    	strvar = "adcwb"
		print(strvar.center(10,"*"))	# **adcwb***
    ljust：填充字符串，原字符串居左显示，默认填充空格
		strvar = "adcwb"
		print(strvar.ljust(10,"*"))	# adcwb*****
	rjust：填充字符串，原字符串居左显示，默认填充空格
    	strvar = "adcwb"
		print(strvar.rjust(10,"*"))	# *****adcwb
    zfile：字符串右对齐显示，不够用0填充，不可指定填充符
    	strvar = "adcwb"
		print(strvar.zfill(10))		#00000adcwb
        
strip：默认去掉两边的空格，也可指定要去掉的符号
	strvar = "    adcwb      "
	print(strvar.strip())	# adcwb
    lstrip：去掉左边的某个字符
    rstrip：去掉右边的某个字符
		strvar = "    adcwb@@@@@@@@"
		print(strvar.strip("@"))	#    adcwb
        
split：按某个指定的字符将字符串分割成列表(默认空格)
	strvar = "a b c d e f "
	print(strvar.split())	#	['a', 'b', 'c', 'd', 'e', 'f']
    rsplit：从右向左切割
    	strvar = "a/b/c/d/e/f"
		print(strvar.rsplit("/",2))		指定分割的次数
        
join：从可迭代对象中取出多个字符串，然后按照指定的分隔符进行拼接，拼接的结果为字符串
	从字符串'hello'中取出多个字符串，然后按照%作为分隔符号进行拼接
    	'%'.join('hello')   >>> 'h%e%l%l%o'

replace：用新的字符替换字符串中旧的字符
	语法：replace(要替换的字符,替换成什么,替换的次数)
	strvar = "hello python"
	print(strvar.replace("python","java"))	# hello java
    	
isinstance：判断类型
	# 用法一
        res = isinstance(5,int)
        res = isinstance("11223344",str)
        res = isinstance([1,2,3],tuple)
        print(res)

    # 用法二
        res = isinstance(16, (str,list,tuple)  )
        print(res)

	
```

### 三、字符串的格式化

```python
format
	顺序传参：
    	print("{}您好，你的账户余额为{}".format("小明"，"18.00"))
        
    索引传参：
    	print("{2}您好，你的账户余额为{1}".format("小明"，"18.00"))
        
	关键字传参：
    	print("{h1}您好，你的账户余额为{h2}".format(h1="小明",h2="18.00"))
    
    容器类型传参：
    	print("{g1[2]}您好，你的账户余额为{g2[2]}".format(g1=["小明", "小红", "小刚"], g2=["18.05", "19.13", "13.14"]))
        format中，不能使用逆向下标，不识别，若容器类型是字典，直接写键值，不需要加上引号
        
        
format填充符号的使用：
	^  原字符串居中
    >  原字符串居右
    <  原字符串居左

    {who:*^10}
    who : 关键字参数
    *   : 要填充的字符
    ^   : 原字符串居中
    10  : 总长度 = 原字符串长度 + 填充字符长度
        strvar = "{who:*^10}在{where:>>10},{do:!<10}".format(who="小明",where="电影院",do="看喜洋洋")			# ****小明****在>>>>>>>电影院,看喜洋洋!!!!!!
        
特殊符号的使用
	:d 整型占位符，要求数据类型必须是整型，否则会抛出异常
        :2d 占用两位，不够两位拿空格来补，默认居右
    :f 浮点型占位符，要求数据类型必须是浮点型，否则会抛出异常
        :.2f 小数点保留2位，默认小数保留六位
    :s 字符串占位符，要求数据类型必须是字符串
    :, 金钱占位符
    	strvar = "{:,}".format(123456789)   123,456,789
    
        
```



### 四、列表相关操作

```python
1.1 列表的拼接(同元组)
	list1 = [1,2,3]
    list2 = [4,5,6]
    res = list1+list2 # [1,2,3,4,5,6]
    
1.2 列表的重复(同元组)
	list1 = [1,2,3]
    list1 * 3 				# [1, 2, 3, 1, 2, 3, 1, 2, 3]
    
1.3 列表的切片(同元组)
	语法 => 列表[::]  完整格式：[开始索引:结束索引:间隔值]
    	(1)[开始索引:]  从开始索引截取到列表的最后
		(2)[:结束索引]  从开头截取到结束索引之前(结束索引-1)
		(3)[开始索引:结束索引]  从开始索引截取到结束索引之前(结束索引-1)
		(4)[开始索引:结束索引:间隔值] 从开始索引截取到结束索引之前按照指定的间隔截取列表元素值
		(5)[:]或[::]  截取所有列表
	
1.4 列表的修改(可切片)
	可以利用切片一次性修改多个元素，没有个数的限制
    切片配合步长，切出多少个元素，修改多少个元素
    
1.5 列表的删除(可切片)
	lst = ["吕洞宾","何仙姑","铁拐李","曹国舅","张果老","蓝采和","韩湘子","汉钟离"]
    del lst[-1]
    print(lst)	# ['吕洞宾', '何仙姑', '铁拐李', '曹国舅', '张果老', '蓝采和', '韩湘子']
    
1.6 列表的相关函数
	append():
        功能：向列表的末尾添加新的元素
        格式：列表.append(值)
        返回值：None
        注意：新添加的值在列表的末尾，该函数直接操作原有列表
        	lst = ["aaa"]
            lst.append("bbb")
            print(lst)
        
	insert():
        功能：在指定索引之前插入元素
        格式：列表.insert(索引,值)
        返回值:None
        注意：直接改变原有列表
        	lst.insert(1,"ccc")
			print(lst)
        
	extend():
        功能：迭代追加所有元素，追加的内容必须是可迭代对象
        格式：列表.extend(可迭代性数据)
        返回值：None
        注意：直接改变原有列表
            aaa = "123"
            lst.extend(aaa)
            print(lst)
        
        
	pop():
        功能：通过指定索引删除元素,若没有索引移除最后那个
        格式：列表.pop(索引)
        返回值：删除的元素
        (注意：没有指定索引，默认移除最后一个元素 )
        	lst = ["aaa","bbb","ccc"]
            res = lst.pop()  # ccc
            res = lst.pop(1)   # bbb 
        
	remove():
    	功能：通过给予的值来删除,如果多个相同元素,默认删除第一个
        格式：列表.remove(值)
        返回值：无
        (注意：如果有索引的情况推荐使用pop,效率高于remove)
            lst = ["aaa","bbb","ccc"]
            lst.remove("aaa")
            print(lst)
        
	clear():
        功能：清空列表
        格式：列表.clear()
        返回值：空列表
            lst = ["aaa","bbb","ccc"]
            lst.clear()
            print(lst)  # []
            
	index():
        功能：获取某个值在列表中的索引
        格式：列表.index(值[,start][,end]) # []  表达参数可选项 
        返回值：找到返回索引  (找不到报错)
            lst = ["aaa","bbb","ccc"]
            res = lst.index("ccc")
            print(res)   # 2
            
	count():
        功能：计算某个元素出现的次数
        格式：列表.count(值)
        返回值：次数
        区别：字符串里面的count 可以划定范围,列表里面的count不行
        	lst = ["aaa", "aaa", "aaa"]
            res = lst.count("aaa")
            print(res)    # 3
        
	sort():
        功能：列表排序(默认小到大排序)
        格式：列表.sort(reverse=False)                        
        返回值：None
        注意：直接更改原列表，按照ascii编进行排序
        	一位一位进行比较,在第一位相同的情况下,比较第二位,以此类推
            可以对中文进行排序，但是没有规律可循
            lst = [44,99,1,10,3,-5,-90]
            lst.sort()
            print(lst)   # [-90, -5, 1, 3, 10, 44, 99]
        	lst.sort(reverse=True)  从大到小排序
            
	reverse()
    	功能：列表反转操作
        格式：列表.reverse()
        返回值：None
        注意：直接更改原列表
            lst = ["aaa", "bbb", "ccc"]
            lst.reverse()
            print(lst)   # ['ccc', 'bbb', 'aaa']
```

### 深浅拷贝

```python
深浅拷贝：
	浅拷贝只拷贝外层列表(一级容器)中的所有数据
    深拷贝是拷贝所有层级的所有元素
    深拷贝在执行时: 如
        果是不可变数据,地址会暂时的指向原来数据,
        如果是可变数据,直接开辟新空间
        
浅copy
	方式一：
        import copy
        lst = ["111", "222", "333"]
        lst1 = copy.copy(lst)
        
	方式二：
    	lst = ["111", "222", "333"]
        lst1 = lst.copy()
        print(lst1)
        
深拷贝：
	import copy
    lst1 = [1,2,3,[4,5,6]]
    lst2 = copy.deepcopy(lst1)
    
    

```

### 元组

```pythom
元组的相关操作除了不能修改和删除其中的元素之外 , 剩下操作都和列表相同.
元组里面能用的方法只有 index 和 count 
```

### 字典

```python
字典相关函数
    fromkeys()
    	使用一组键和默认值创建字典
            dic_var = {}
            dic_var["key"] = "value"   #添加单个元素
            print(dic_var) 
            
            dic_var = {}.fromkeys(lst, None)
			print(dic_var)  # {'aa': None, 'bb': None, 'cc': None}
            
    pop()       
    	通过键去删除键值对 (若没有该键可设置默认值,预防报错)，并返回值
            dic = {'k1': 'jason', 'k2': 'Tony', 'k3': 'JY'}
            reg = dic.pop("k1")
            print(reg)
            
    popitem()   
    	删除最后一个键值对
        	dic = {'k1': 'jason', 'k2': 'Tony', 'k4': 'JY'}
            item = dic.popitem()
            print(dic)      # {'k1': 'jason', 'k2': 'Tony'}
            print(item)     #  ('k4', 'JY')
            
    clear()  
    	清空字典
            dic = {'k1': 'jason', 'k2': 'Tony', 'k4': 'JY'}
            dic.clear()
            print(dic)
            
    update() 
    	批量更新(有该键就更新,没该键就添加)
        	dic= {'k1':'jason','k2':'Tony','k3':'JY'}
            dic.update({'k1':'JN','k4':'xxx'})
            print(dic)  # {'k1': 'JN', 'k2': 'Tony', 'k3': 'JY', 'k4': 'xxx'} 
            
    get()    
    	通过键获取值(若没有该键可设置默认值,预防报错)
        	dic= {'k1':'jason','k2':'Tony','k3':'JY'}
            dic.get('k1')   # jason
            res=dic.get('xxx',666) # key不存在时，可以设置默认返回的值
            print(res)   # 666
            
    keys()   
    	将字典的键组成新的可迭代对象
        	dic= {'k1':'jason','k2':'Tony','k3':'JY'}
            print(dic.keys())  # dict_keys(['k1', 'k2', 'k3'])
            print(dic.values()) # dict_values(['jason', 'Tony', 'JY'])
                
    values() 
    	将字典中的值组成新的可迭代对象
        	dict_items([('k1', 'jason'), ('k2', 'Tony'), ('k3', 'JY')])
            
    items()  
    	将字典的键值对凑成一个个元组,组成新的可迭代对象 
        	print(dic.items()) 
            	#  dict_items([('k1', 'jason'), ('k2', 'Tony'), ('k3', 'JY')])
                
	setdefault()
    	key不存在则新增键值对，并将新增的value返回
        	dic={'k1':111,'k2':222}
            res=dic.setdefault('k3',333)
            print(res)  # 333
            print(dic)  # {'k1': 111, 'k3': 333, 'k2': 222}
```

### 集合

```python
集合、list、tuple、dict一样都可以存放多个值，但是集合主要用于：去重、关系运算
定义：在{}内用逗号分隔开多个元素，集合具备以下三个特点：
     1：每个元素必须是不可变类型
     2：集合内没有重复的元素
     3：集合内元素无序
	注意：列表类型是索引对应值，字典是key对应值，均可以取得单个指定的值，而集合类型既没有索引也没有key与值对应，所以无法取得单个的值，而且对于集合来说，主要用于去重与关系元素，根本没有取出单个指定值这种需求。
    s = set() # 定义空集合
    
集合中的交差并补
    intersection() 交集，简写 & 
    difference()   差集，简写 -   
    union()  并集，简写 |         
    symmetric_difference() 对称差集 (补集情况涵盖在其中)  简写^
    issubset()   判断是否是子集 简写<
    issuperset() 判断是否是父集 简写>=
    isdisjoint() 检测两集合是否不相交  不相交 True  相交False
    
        # 1.合集/并集(|)：求两个用户所有的好友（重复好友只留一个）
        print(friends1 | friends2)  #{'zero', 'jason', 'Jy', 'ricky', 'egon', 'kevin'}
        # 2.交集(&)：求两个用户的共同好友
        print(friends1 & friends2) # {'jason', 'egon'}
        # 3.差集(-)：
        print(friends1 - friends2)  # {'zero', 'kevin'}
        print(friends2 - friends1)  # {'Jy', 'ricky'}
        # 4.对称差集(^) # 求两个用户独有的好友们（即去掉共有的好友）
        print(friends1 ^ friends2)  # {'zero', 'Jy', 'ricky', 'kevin'}
        # 5.值是否相等(==)
        print(friends1 == friends2) # False
        # 6.父集：一个集合是否包含另外一个集合
        print({1,2,3} > {1,2}) # True
        print({1,2,3} > {1,3,4,5}) # False
        # 7.子集
        print({1,2} < {1,2,3}) #True
        print({1,2} <= {1,2,3}) #True
    
集合相关函数
    add()    向集合中添加数据
		set_var = {"aaa", "bbb", "ccc"}
        set_var.add("ddd")
        print(set_var)
    update() 迭代着增加
    	set_var = {"aaa", "bbb", "ccc"}
        svr = ("111", "222")
        set_var.update(svr)
        print(set_var)
    clear()  清空集合
    	set_var = {"aaa", "bbb", "ccc"}
        set_var.clear()
        
    pop()    随机删除集合中的一个数据
    	set_var = {"aaa", "bbb", "ccc"}
        set_var.pop()
        print(set_var)
        
    remove()  删除集合中指定的值(不存在则报错)
    	set_var = {"aaa", "bbb", "ccc"}
        set_var.remove("aaa")
        print(set_var)

    discard() 删除集合中指定的值(不存在的不删除 推荐使用)
		set_var = {"aaa", "bbb", "ccc"}
        set_var.discard("123")
        print(set_var)

冰冻集合
#frozenset 可强转容器类型数据变为冰冻集合
冰冻集合一旦创建,不能在进行任何修改,只能做交叉并补操作
	set_var = ["aaa", 123, "ccc"]
    set_var1 = frozenset(set_var)
    print(set_var1, type(set_var1))
    
```

### 可变不可变类型

```python
可变类型：
    值发生改变时，内存地址不变，即id不变，证明在改变原值
    列表，字典，set(集合)
不可变类型集合：
    值发生改变时，内存地址也发生改变，即id也变，证明是没有在改变原值，是产生了新的值
    数字，字符串，元组

```

