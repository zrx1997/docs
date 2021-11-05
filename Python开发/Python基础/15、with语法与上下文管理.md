### 上下文管理器（Context Manager）

​		上下文管理器是指在一段代码执行之前执行一段代码，用于一些预处理工作；执行之后再执行一段代码，用于一些清理工作。比如打开文件进行读写，读写完之后需要将文件关闭。又比如在数据库操作中，操作之前需要连接数据库，操作之后需要关闭数据库。在上下文管理协议中，有两个方法__enter__和__exit__，分别实现上述两个功能。



### with语法

```python
基本语法：
	with EXPR as VAR:
    	BLOCK
执行过程：
	（1）执行EXPR语句，获取上下文管理器（Context Manager）

    （2）调用上下文管理器中的__enter__方法，该方法执行一些预处理工作。

    （3）这里的as VAR可以省略，如果不省略，则将__enter__方法的返回值赋值给VAR。

    （4）执行代码块BLOCK，这里的VAR可以当做普通变量使用。

    （5）最后调用上下文管理器中的的__exit__方法。

    （6）__exit__方法有三个参数：exc_type, exc_val, exc_tb。如果代码块BLOCK发生异常并退出，那么分别对应异常的type、value 和 traceback。否则三个参数全为None。

    （7）__exit__方法的返回值可以为True或者False。如果为True，那么表示异常被忽视，相当于进行了try-except操作；如果为False，则该异常会被重新raise。
        
```

#### 案例：打开文件操作

```python
# 自定义打开文件操作

class MyOpen(object):
    def __init__(self, filename):
        """初始化构造方法"""
		self.filename = filename
        self.file_hander = None
        return
    
    def __enter__(self):
        """enter方法，返回file_handler"""
        print("enter:", self.file_name)
        self.file_handler = open(self.file_name, "r")
        return self.file_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit方法，关闭文件并返回True"""
        print("exit:", exc_type, exc_val, exc_tb)
        if self.file_handler:
            self.file_handler.close()
        return True



with MyOpen("python_base.py") as file_in:
    for line in file_in:
        print(line)
        raise ZeroDivisionError
# 代码块中主动引发一个除零异常，但整个程序不会引发异常



```

#### contexlib库的使用

​		Python提供内置的contextlib库，使得上线文管理器更加容易使用。其中包含如下功能：

```	Python
	（1）装饰器contextmanager。该装饰器将一个函数中yield语句之前的代码当做__enter__方法执行，yield语句之后的代码当做__exit__方法执行。同时yield返回值赋值给as后的变量。

    @contextlib.contextmanager
    def open_func(file_name):
        # __enter__方法
        print('open file:', file_name, 'in __enter__')
        file_handler = open(file_name, 'r')

        yield file_handler

        # __exit__方法
        print('close file:', file_name, 'in __exit__')
        file_handler.close()
        return

    with open_func('python_base.py') as file_in:
        for line in file_in:
            print(line)

	（2）closing类。该类会自动调用传入对象的close方法。使用实例如下：
        class MyOpen2(object):
            def __init__(self, file_name):
                """初始化方法"""
                self.file_handler = open(file_name, "r")
                return

            def close(self):
                """关闭文件，会被自动调用"""
                print("call close in MyOpen2")
                if self.file_handler:
                    self.file_handler.close()
                    return

		with contextlib.closing(MyOpen2("python_base.py")) as file_in:
			pass
```

