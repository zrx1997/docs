## 装饰器

```python
装饰器：

    什么是装饰器：
        '装饰'代指为被装饰对象添加新的功能，'器'代指器具/工具，装饰器与被装饰的对象均可以是任意可调用对象。概括地讲，装饰器的作用就是在不修改被装饰对象源代码和调用方式的前提下为被装饰对象添加额外的功能。
        
    为何要用装饰器：
        开放封闭原则：
            开放：指的是对拓展功能是开放的
            封闭：指的是对修改源代码是封闭的
		装饰器就是在不修改被装饰器对象源代码以及调用方式的前提下为被装饰对象添加新功能

	语法糖：
		在Python语法中，为了更简洁而优雅的使用装饰器，专门提供了一种语法来取代index=timer(index)的形式，需要在被装饰对象的正上方单独一行添加@timer,当解释器解释到@timer时就会调用timer函数，且把它正下方的函数名当做实参传入，然后将返回的结果重新赋值给原函数名
                @timer # index=timer(index)
                def index():
                    time.sleep(3)
                    print('Welcome to the index page')
                    return 200
            如果在一个函数中需要使用多个装饰器，可以叠加调用，叠加多个装饰器也无特殊之处
            加载顺序自上而下，执行顺序自上而下
                @deco3
                @deco2
                @deco1
                def index():
                    pass
            等同于index=deco3(deco2(deco1(index)))

        装饰器的实现原理有一些类似于偷梁换柱的概念，即将原函数名指向的内存地址偷梁换柱成warpper函数，因此应该将warpper做的和原函数一样才行
            
            
    装饰器的使用：
        函数装饰器分为：无参装饰器和有参装饰两种，二者的实现原理一样，都是’函数嵌套+闭包+函数对象’的组合使用的产物。
        无参装饰器;
            需求：在不修改index函数的源代码以及调用方式的前提下为其添加统计运行时间的功能
                def index(x,y):
                    time.sleep(3)
                    print('index %s %s' %(x,y))

                index(111,222)
                
            实现：
                def times(func):
                    def warpper(*args,**kwargs):
                        start_time = time.time()
                        res = func(*args,**kwargs)
                        stop_time = time.time()
                        print('run time is %s' %(stop_time - start_time))
                        return  res
                    return warpper
                
			无参装饰器模板：
                def outter(func):
                    def wrapper(*args,**kwargs):
                        # 1、调用原函数
                        # 2、为其增加新功能
                        res=func(*args,**kwargs)
                        return res
                    return wrapper


        有参装饰器：
            由于语法糖@的限制，outter函数只能有一个参数，并且该参数只用来接收被装饰对象的内存地址
            有参装饰器模板：
                def 有参装饰器(x,y,z):
                    def outter(func):
                        def wrapper(*args, **kwargs):
                            res = func(*args, **kwargs)
                            return res
                        return wrapper
                    return outter

                @有参装饰器(1,y=2,z=3)
                def 被装饰对象():
                    pass
        可以使用help来查看函数的文档注释，本质就是查看函数的doc属性，但是对于被装饰之后的函数，查看文档注释
            print(help(home))
        打印结果：
                Help on function wrapper in module __main__:
                wrapper(*args, **kwargs)
                None
                
        若想要保留原函数的文档和函数名属性，需要修正装饰器
            def timer(func):
                def wrapper(*args,**kwargs):
                    start_time=time.time()
                    res=func(*args,**kwargs)
                    stop_time=time.time()
                    print('run time is %s' %(stop_time-start_time))
                    return res
                wrapper.__doc__=func.__doc__
                wrapper.__name__=func.__name__
                return wrapper
            
        手动将原函数的属性赋值给warpper函数：
                1、函数wrapper.__name__ = 原函数.__name__
                2、函数wrapper.__doc__ = 原函数.__doc__
                wrapper.__name__ = func.__name__
                wrapper.__doc__ = func.__doc__

        Python中有一个专门的模块functools下提供了一个装饰器warps专门用来帮我们实现这件事
            from functools import wraps

            def timer(func):
                @wraps(func)
                def wrapper(*args,**kwargs):
                    start_time=time.time()
                    res=func(*args,**kwargs)
                    stop_time=time.time()
                    print('run time is %s' %(stop_time-start_time))
                    return res
                return wrapper


    装饰器的叠加：
        由下至上依次执行
        先执行最下面的装饰器函数，然后把结果在传给上面的装饰器

	类装饰器：
    	无参类装饰器：
        	class Kuozhan():
                def __call__(self, func):           # 把对象当作函数调用的时候自动触发
                    return self.kuozhan2(func)

                def kuozhan1(func):
                    def newfunc():
                        print("考试前，认真复习")
                        func()
                        print("考试后，咋咋呼呼")
                    return newfunc

                def kuozhan2(self,func):
                    def newfunc():
                        print("考试前，开开心心")
                        func()
                        print("考试后，又哭又闹")
                    return newfunc

            @Kuozhan.kuozhan1
            def func():
                print("考试中......")

            func()
            print(">>>>>>>>>>>>>>>>>")
            @Kuozhan()
            def func():
                print("考试中......")
            func()

		有参类装饰器：
        	class Kuozhan():
                money = "故宫门票，每人100一次，"

                def __init__(self,num):
                    self.num = num

                def __call__(self, cls):
                    if self.num == 1:
                        return self.newfunc1(cls)
                    elif self.num == 2:
                        return self.newfunc2(cls)

                def ad(self):
                    print("故宫一般指北京故宫。北京故宫是中国明清两代的皇家宫殿，旧称紫禁城，位于北京中轴线的中心。北京故宫以三大殿为中心....")

                def newfunc1(self,cls):
                    def newfunc():
                        cls.money = Kuozhan.money
                        cls.ad = Kuozhan.ad
                        return cls()
                    return newfunc

                def newfunc2(self,cls):
                    def newfunc():
                        if "run" in cls.__dict__:
                            res = cls.run()
                            cls.run = res
                            return cls()
                    return newfunc

            @Kuozhan(1)
            class MyClass():
                def run():
                    return "程序运行成功。。。"


            obj = MyClass()
            print(obj.money)
            obj.ad()

            @Kuozhan(2)
            class MyClass():
                def run():
                    return "程序运行成功。。。"


            obj = MyClass()
            print(obj.run)
```

## 迭代器

```python
迭代器：
    什么是迭代器：
        迭代器指的是迭代取值的工具，迭代是一个重复的过程，每次重复都是基于上一次的结果而继续的，单纯的重复并不是迭代
        
    为何要有迭代器：
        迭代器是用来迭代取值的工具，而涉及到把多个值循环取出来的类型有：列表、字符串、元组、字典、集合、打开文件
        上述迭代取值的方式只适用于有索引的数据类型：列表、字符串、元组，为了解决基于索引迭代器取值的局限性python必须提供一种能够不依赖于索引的取值方式，这就是迭代器

    迭代器的使用：
        可迭代对象：
            从语法形式上讲，内置有__iter__方法的对象都是可迭代对象
            调用可迭代对象下的__iter__方法会将其转换成迭代器对象
            字符串、列表、元组、字典、集合、打开的文件都是可迭代对象
			dir方法获取当前类型对象中的所有成员
        迭代器对象：
            迭代器对象是内置有iter和next方法的对象，打开的文件本身就是一个迭代器对象，执行迭代器对象.iter()方法得到的仍然是迭代器本身，而执行迭代器.next()方法就会计算出迭代器中的下一个值。 迭代器是Python提供的一种统一的、不依赖于索引的迭代取值方式，只要存在多个“值”，无论序列类型还是非序列类型都可以按照迭代器的方式取值

        for循环原理：
            for循环可以称之为叫迭代器循环
            使用while循环实现for循环的效果：
                goods=['mac','lenovo','acer','dell','sony']
                i=iter(goods) #每次都需要重新获取一个迭代器对象
                while True:
                    try:
                        print(next(i))
                    except StopIteration: #捕捉异常终止循环
                        break

            迭代器取值：
                1、d.__iter__()得到一个迭代器对象
                2、迭代器对象.__next__()拿到一个返回值，然后将该返回值赋值给k
                3、循环往复步骤2，直到抛出StopIteration异常for循环会捕捉异常然后结束循环

            for循环又称为迭代循环，in后可以跟任意可迭代对象，上述while循环可以简写为
                goods=['mac','lenovo','acer','dell','sony']
                for item in goods:   
                    print(item)
            for 循环在工作时，首先会调用可迭代对象goods内置的iter方法拿到一个迭代器对象，然后再调用该迭代器对象的next方法将取到的值赋给item,执行循环体完成一次循环，周而复始，直到捕捉StopIteration异常，结束迭代。

        迭代器的优缺点：
            优点：
                1、为序列和非序列类型提供了一种统一的迭代取值方式
                2、惰性计算：迭代器对象表示的是一个数据流，可以只在需要时才去调用next来计算出一个值，就迭代器本身来说，同一时刻在内存中只有一个值，因而可以存放无限大的数据流，而对于其他容器类型，如列表，需要把所有的元素都存放于内存中，受内存大小的限制，可以存放的值的个数是有限的。
            缺点：
                1、除非取尽，否则无法获取迭代器的长度
                2、只能取下一个值，不能回到开始，更像是‘一次性的’，迭代器产生后的唯一目标就是重复执行next方法直到值取尽，否则就会停留在某个位置，等待下一次调用next；若是要再次迭代同个对象，你只能重新调用iter方法去创建一个新的迭代器对象，如果有两个或者多个循环使用同一个迭代器，必然只会有一个循环能取到值


```

## 生成器

```python
生成器：
    如何得到自定义的迭代器：
        在函数内若存在yield关键字，调用函数并不会执行函数体代码，会返回一个生成器对象，生成器即自定义的迭代器
        生成器内置有__iter__和__next__方法，所以生成器本身就是一个迭代器

    next方法会触发函数体代码的执行，然后遇到yield停下来，将yield后的值当做本次调用的结果返回

    有了yield关键字，我们就有了一种自定义迭代器的实现方式。yield可以用于返回值，但不同于return，函数一旦遇到return就结束了，而yield可以保存函数的运行状态挂起函数，用来返回多次值

    yield表达式：
        在函数内可以采用表达式形式的yield
            def eater():
                print('Ready to eat')
                while True:
                    food = yield
                    print('get the food: %s, and start to eat' %food)
        可以拿到函数的生成器对象持续为函数体send值
            g = eater()
            print(g)
            g.send(None)       #等同于next(g)，刚启动的生成器第一次传入的值不能是非空
            g.send('aaa')
        针对表达式形式的yield，生成器对象必须事先被初始化一次，让函数挂起在food=yield的位置，等待调用g.send()方法为函数体传值。

        表达式形式的yield也可以用于返回多次值，即变量名=yield 值的形式
            def eater():
                print('Ready to eat')
                food_list = []
                while True:
                    food = yield food_list
                    food_list.append(food)
        也可以编写装饰器来完成为所有表达式形式yield对应生成器的初始化操作
            def init(func):
                def wrapper(*args,**kwargs):
                    g=func(*args,**kwargs)
                    next(g)
                    return g
                return wrapper

            @init
            def eater():
                print('Ready to eat')
                while True:
                    food=yield
                    print('get the food: %s, and start to eat' %food)
    三元表达式：
        三元表达式是python为我们提供的一种简化代码的解决方案，语法如下
            res = 条件成立时返回的值  if  条件  else  条件不成立时返回的值
            例：
                def max2(x,y):
                    if x > y:
                        return x
                    else:
                        return y

                res = max2(1,2)
            使用三元表达式
                res = x if x > y else y   # 三元表达式
    列表生成式：
        列表生成式是python为我们提供的一种简化代码的解决方案，用来快速生成列表，语法如下
            [expression for item1 in iterable1 if condition1
            for item2 in iterable2 if condition2
            ...
            for itemN in iterableN if conditionN
            ]
        例：
            l = ['alex_dsb', 'lxx_dsb', 'wxx_dsb', "xxq_dsb", 'egon']
            new_l=[]
            for name in l:
                if name.endswith('dsb'):
                    new_l.append(name)

        利用列表生成式：
            new_l=[name for name in l if name.endswith('dsb')]
            new_l=[name for name in l]

    字典生成式：
        keys=['name','age','gender']
        dic={key:None for key in keys}
        print(dic)

        items=[('name','egon'),('age',18),('gender','male')]
        res={k:v for k,v in items if k != 'gender'}
        print(res)

    集合生成式：
        keys=['name','age','gender']
        set1={key for key in keys}
        print(set1,type(set1))

    生成器表达式：
        g=(i for i in range(10) if i > 3)    #此时g内一个值都没有
        print(g,type(g))
        print(next(g))    #每次调用返回一个值

    案例：统计文件大小
        with open('笔记.txt', mode='rt', encoding='utf-8') as f:
            # 方式一：
            # res=0
            # for line in f:
            #     res+=len(line)
            # print(res)

            # 方式二：
            # res=sum([len(line) for line in f])
            # print(res)

            # 方式三 ：效率最高
            # res = sum((len(line) for line in f))
            # 上述可以简写为如下形式
            res = sum(len(line) for line in f)
            print(res)

```

## 递归函数

```python
函数递归调用：
    函数不仅可以嵌套定义，还可以嵌套调用，即在调用一个函数的过程中，函数内部又调用另一个函数
    而函数的递归调用指的是在调用一个函数的过程中又直接或间接地调用该函数本身
    直接调用本身：
        def f1():
            print('===>f1')
            f1()
    间接调用本身：
        def f1():
            print('===>f1')
            f2()

        def f2():
            print('===>f2')
            f1()
        f1()
    递归的本质就是循环
    递归调用不应该无限地调用下去，必须在满足某种条件下结束递归调用
    注：
        1、可以使用sys.getrecursionlimit()去查看递归深度，默认值为1000，虽然可以使用
        2、python不是一门函数式编程语言，无法对递归进行尾递归优化

回溯与递推：
    回溯：一层一层调用下去
    递推：满足某种结束条件，结束递归调用，然后一层一层返回

案例：
    l=[1,2,[3,[4,[5,[6,[7,[8,[9,10,11,[12,[13,]]]]]]]]]]

    def f1(list1):
        for x in list1:
            if type(x) is list:
                # 如果是列表，应该再循环、再判断,即重新运行本身的代码
                f1(x)
            else:
                print(x)

    f1(l)


```

## 匿名函数

```python
lambda 函数表达式:  只实现一些简单的函数功能,但是写法非常简便
	func = lambda x,y:x*y
    lambda 参数：	实现的功能
    
```

## 高阶函数

```python
什么是高阶函数:
	一个函数可以作为参数传给另外一个函数，或者一个函数的返回值为另外一个函数（若返回值为该函数本身，则为递归），满足其一则为高阶函数。

# map
map(func,iterable)
功能:
	把iterable里面所有数据 一一的放进到func这个函数中进行操作 ,把结果扔进迭代器
参数:
	func  内置或自定义函数
	iterable 具有可迭代性的数据 ([迭代器],[容器类型的数据],[range对象])
返回值: 
	返回最后的迭代器
        num=[1,2,3,4,5]
        def square(x):
            return x**2
        #map函数模拟
        def map_test(func,iter):
            num_1=[]
            for i in iter:
                ret=func(i)
                # print(ret)
                num_1.append(ret)
            return num_1.__iter__() #将列表转为迭代器对象

        #map_test函数
        print(list(map_test(square,num)))
        #map函数
        print(list(map(square,num)))

        #当然map函数的参数1也可以是匿名函数、参数2也可以是字符串
        print(list(map_test(lambda x:x.upper(),"amanda")))
        print(list(map(lambda x:x.upper(),"amanda")))


# reduce
reduce(func,iterable)
功能:   
    先把iterable里面的前2个数据拿到func函数当中进行运算,得到结果,
    在把计算的结果和iterable中的第三个数据拿到func里面进行运算,
    依次类推 ,直到iterable里面的所有数据都拿完为止,程序结束
参数:
	func     内置或自定义函数
	iterable 具有可迭代性的数据 ([迭代器],[容器类型的数据],[range对象])
返回值: 
	计算的最后结果
    	#reduce函数不是内置函数，而是在模块functools中的函数，故需要导入
        from functools import reduce

        nums=[1,2,3,4,5,6]
        #reduce函数的机制
        def reduce_test(func,array,ini=None): #ini作为基数
            if ini == None:
                ret =array.pop(0)
            else:
                ret=ini
            for i in array:
                ret=func(ret,i)
            return ret
        #reduce_test函数，叠乘
        print(reduce_test(lambda x,y:x*y,nums,100))
        #reduce函数，叠乘
        print(reduce(lambda x,y:x*y,nums,100))


# sorted 
sorted(iterable,reverse=False,key=函数)
功能:  
	对数据进行排序
参数: 
    iterable  : 具有可迭代性的数据(迭代器,容器类型数据,可迭代对象)
    reverse   : 是否反转 默认为False 代表正序, 改成True 为倒序
    key       : 指定函数 内置或自定义函数
返回值:
	返回排序后的数据


# filter
filter(func,iterable)
功能:
    用来过滤的,如果func函数中返回True , 会将这个值保留到迭代器中
    如果func函数中返回False , 会将此值舍弃不保留
参数:
    func : 自定义函数
    iterable : 具有可迭代性的数据(迭代器,容器类型数据,可迭代对象)
返回值: 
	返回处理后的迭代器
        names=["Alex","amanda","xiaowu"]
        #filter函数机制
        def filter_test(func,iter):
            names_1=[]
            for i in iter:
                if func(i): #传入的func函数其结果必须为bool值，才有意义
                    names_1.append(i)
            return names_1
        #filter_test函数
        print(filter_test(lambda x:x.islower(),names))
        #filter函数
        print(list(filter(lambda x:x.islower(),names)))

```

