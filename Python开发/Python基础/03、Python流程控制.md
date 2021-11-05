if语句

```python
if语句基本语法：
    if    判断条件:                                                                         		符合条件执行的动作
    elif   判断条件:  
        执行的动作                                                                 
    else:
        执行的动作
			
	Python语言中，为了区分if语句中判断条件执行时和else区分，所以要求缩进，而别的语言由于有大括号进行区分，所以不需要缩进，执行的动作可以有多条；tab键不等于四个空格，缩进级别必须要保持一致；官方规定缩进四个空格；此外，if语句由上到下判断，当有一个条件判断成功后，其他的语句不再判断
			
	if语句可以无限的嵌套. 但是在实际开发中. 尽量不要超过三层嵌套
			
    示例：
        age = 19
        is_beautiful = True
        star = '水平座'

        if 18 < age < 20 and is_beautiful and star == '水平座':
            print('开始表白。。。。。')
            is_successful = True
            if is_successful:
                print('两个从此过上没羞没臊的生活。。。')
        elif 10 < age <18: 
            print('你太小了，我们不合适。。。。')

        else:
            print('阿姨好，我逗你玩呢，深藏功与名')
        print('对不起，系统无法确认性别。。。。')

```

while循环

```python
whihe循环：

    基本语法：
        while   条件：
            代码
        else：
            代码

    退出while循环的两种方式
        方式一：
            将条件改为false，等到下次循环判断条件时才会生效
        方式二：
            break，只要遇到break就会立刻终止本次循环
            continue：结束本轮循环，直接进入下次循环
            注：在continue之后添加同级代码毫无意义，因为永远无法运行

    while循环可以嵌套，但是要注意层级
    while循环和else连用的时候，while循环必须是在没有被break打断的情况下，才可以运行
        count=0
        while count < 3:
            inp_name=input('请输入您的账号：')
            inp_pwd=input('请输入您的密码：')

            if inp_name  == username and inp_pwd == password:
                print('登录成功')
                while True:
                    cmd=input("输入命令>: ")
                    if cmd == 'q': # 整个程序结束，退出所有while循环
                        break
                    else:
                        print('命令{x}正在运行'.format(x=cmd))
                break
            else:
                print('账号名或密码错误')
                count+=1
        else:
            print('输错3次，退出')
			

```

for循环

```python
for循环：
    for 变量名 in 可迭代对象:# 可迭代对象可以是：列表、字典、字符串、元组、集合
        代码1
        代码2
        代码3

    range(10)                                  #打印1到10
    range（1,9,1）                        #打印1到9每次递增1
        for搭配range，可以按照索引取值，但是麻烦，所以不推荐
    for循环嵌套
        外层循环循环一次，内层循环需要完整的循环完毕
        终止for循环只有break一种方案
    for+break：
        终止循环
    for+continue：
        终止本次循环
    for+else：
        for循环执行完毕，没有被break和continue打断的情况下，执行else分支的代码
	

```

