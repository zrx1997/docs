### go语言简介



### 安装

```bash
Linux:
	wget https://golang.org/dl/go1.16.3.linux-amd64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    go version

windows:
	https://golang.org/dl/go1.16.3.windows-amd64.msi
    需要添加两个环境变量
    	GOPATH：go项目的根目录
        GOROOT：go解释器安装目录

macos:
	https://golang.org/dl/go1.16.3.darwin-amd64.pkg

source:
	https://golang.org/dl/go1.16.3.src.tar.gz
        
Go开发编辑器
	Go采用的是UTF-8编码的文本文件存放源代码，理论上使用任何一款文本编辑器都可以做Go语言开发，这里推荐使用VS Code和Goland。 VS Code是微软开源的编辑器，而Goland是jetbrains出品的付费IDE。
	
Go项目结构
	在进行Go语言开发的时候，我们的代码总是会保存在GOPATH/src目录下。在工程经过go build、go install或go get等指令后，会将下载的第三方包源代码文件放在GOPATH/src目录下， 产生的二进制可执行文件放在 GOPATH/bin目录下，生成的中间缓存文件会被保存在 GOPATH/pkg 下。
	
	如果我们使用版本管理工具（Version Control System，VCS。常用如Git）来管理我们的项目代码时，我们只需要添加GOPATH/src目录的源代码即可。bin 和 pkg 目录的内容无需版本控制。
```



常见的go开发目录

![image-20210421090556614](https://raw.githubusercontent.com/adcwb/storages/master/image-20210421090556614.png)

适合个人的开发目录

![image-20210421090633849](https://raw.githubusercontent.com/adcwb/storages/master/image-20210421090633849.png)



适合企业开发者的目录结构

![image-20210421090659491](https://raw.githubusercontent.com/adcwb/storages/master/image-20210421090659491.png)

### go程序

```go
// 第一个go程序
// 在GOPATH/src目录下新建文件夹，作为项目的根目录，然后新建main.go

package main  // 声明main包，表明当前是一个可执行程序

import "fmt"  // 导入内置 fmt 包

func main(){  // main函数，是程序执行的入口
    fmt.Println("Hello World!")  // 在终端打印 Hello World!
}

// 常用指令
go build
	表示将源代码编译成可执行文件
	也可直接指定项目名，编译器会去GOPATH的src目录下查找你要编译的项目
		如：go build test1
	使用-o参数来指定编译后可执行文件的名字
		如：go build -o haha.exe

go install
	表示安装的意思，它先编译源代码得到可执行文件，然后将可执行文件移动到GOPATH的bin目录下。因为我们的环境变量中配置了GOPATH下的bin目录，所以我们就可以在任意地方直接执行可执行文件了。


// 跨平台编译
	由于go build生成的可执行文件都是当前系统的可执行文件，所以想要跨平台编译需要指定一些额外的参数

	Windows--> linux64
		SET CGO_ENABLED=0  // 禁用CGO
        SET GOOS=linux  // 目标平台是linux
        SET GOARCH=amd64  // 目标处理器架构是amd64

	Windows--> Mac64
		SET CGO_ENABLED=0
        SET GOOS=darwin
        SET GOARCH=amd64

	Mac 下编译 Linux 和 Windows平台 64位 可执行程序：
		CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build
		CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build

	Linux 下编译 Mac 和 Windows 平台64位可执行程序：
		CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build
		CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build

```



### 变量与常量

#### 标识符

```go
	在编程语言中标识符就是程序员定义的具有特殊意义的词，比如变量名、常量名、函数名等等。 
	Go语言中标识符由字母数字和_(下划线）组成，并且只能以字母和_开头。 
		例如：abc, _, _123, a123。
```

#### 关键字

```go

关键字是指编程语言中预先定义好的具有特殊含义的标识符。 关键字和保留字都不建议用作变量名。

Go语言中有25个关键字：

    break        default      func         interface    select
    case         defer        go           map          struct
    chan         else         goto         package      switch
    const        fallthrough  if           range        type
    continue     for          import       return       var

此外，Go语言中还有37个保留字。

    Constants:    true  false  iota  nil

        Types:    int  int8  int16  int32  int64  
                  uint  uint8  uint16  uint32  uint64  uintptr
                  float32  float64  complex128  complex64
                  bool  byte  rune  string  error

    Functions:   make  len  cap  new  append  copy  close  delete
                 complex  real  imag
                 panic  recover
```

#### 变量

```go
变量：
	程序运行过程中的数据都是保存在内存中，我们想要在代码中操作某个数据时就需要去内存上找到这个变量，但是如果我们直接在代码中通过内存地址去操作变量的话，代码的可读性会非常差而且还容易出错，所以我们就利用变量将这个数据的内存地址保存起来，以后直接通过这个变量就能找到内存上对应的数据了。


变量的类型：
	变量（Variable）的功能是存储数据。不同的变量保存的数据类型可能会不一样。经过半个多世纪的发展，编程语言已经基本形成了一套固定的类型，常见变量的数据类型有：整型、浮点型、布尔型等。

	Go语言中的每一个变量都有自己的类型，并且变量必须经过声明才能开始使用。

变量的声明：
	Go语言中的变量需要声明后才能使用，同一作用域内不支持重复声明。 
	并且Go语言的变量声明后必须使用。
	Go语言的变量声明方式有两种，标准声明和批量声明

标准声明：
	Go语言的变量声明格式为：
		var 变量名 变量类型

    变量声明以关键字var开头，变量类型放在变量的后面，行尾无需分号。 举个例子：
        var name string
        var age int
        var isOk bool

批量声明：
	每声明一个变量就需要写var关键字会比较繁琐，因此go语言中提供了批量变量声明
        var (
                a string
                b int
                c bool
                d float32
            )
```



#### 变量的初始化

```go
	Go语言在声明变量的时候，会自动对变量对应的内存区域进行初始化操作。每个变量会被初始化成其类型的默认值，例如： 整型和浮点型变量的默认值为0。 字符串变量的默认值为空字符串。 布尔型变量默认为false。 切片、函数、指针变量的默认为nil。

	当然我们也可在声明变量的时候为其指定初始值。变量初始化的标准格式如下：
		var 变量名 类型 = 表达式
	例如：
		var name string = "Timi"
		var age int = 18

	也可以一次性初始化多个变量：
		var name, age = "Timi", 20

类型推导：
	有些时候我们会把声明的变量类型省略，这个时候编译器会根据等号右边的值来推导变量的类型完成初始化
			var name = "Timi"
			var age = 18
	
```



#### 短变量声明

```go
在函数内部，可以使用更简略的 := 方法来声明并初始化变量
短变量声明方式只能用于函数内部局部变量，不能在函数外使用
在函数外声明变量，需要使用 var 语句。如果使用了短变量声明方式会导致编译错误。

例：在函数外使用短变量
    package main

    import (
        "fmt"
    )

    hi := "hello" // 编译错误，syntax error: non-declaration statement outside function body

    func main() {
        hi := "hello"
        fmt.Println(hi) // hello
    }

短变量声明语句中至少要声明一个新的变量
短变量声明也可以使用函数的返回值进行声明和初始化。
重复使用短变量声明时，需要保证短变量声明语句中至少要声明一个新的变量，否则直接使用赋值语句 = 就可以了

```



#### 匿名变量

```go
	在使用多重赋值的时候，如果想要忽略某个值，可以使用匿名变量（anonymous variable）。 匿名变量用一个下划线_表示

	匿名变量不占用命名空间，不会分配内存，所以匿名变量之间不存在重复声明。 (在Lua等编程语言里，匿名变量也被叫做哑元变量。)
        func foo() (int, string) {
            return 10, "Timi";
        }
        func main() {
            x, _ := foo()
            _, y := foo()
            fmt.Println("x=", x)
            fmt.Println("y=", y)
        }

注意：
	函数外的每个语句都必须以关键字开始（var、const、func等）
    :=不能使用在函数外。
    _多用于占位，表示忽略值。
	

```

#### 常量

```go
	相对于变量来说，常量是恒定不变的值，多用于程序运行期间不会改变的值，常量的声明和变量声明非常类似，只是把关键字var换成了const， 常量在定义的时候必须赋值
		const pi = 3.14159
		const e = 2.7182

	go语言同样支持多个常量一起声明
        const (
            pi = 3.1415
            e = 2.7182
        )

    const同时声明多个常量时，如果省略了值则表示和上面一行的值相同。 例如：

        const (
            n1 = 100
            n2
            n3
        )

		常量n1、n2、n3的值都是100。
	
```

#### iota

```go
iota是一个古希腊字母.在golang中表示常量计数器.

使用的规则如下:
    每当const出现时, 都会使iota初始化为0.
    const中每新增一行常量声明将使iota计数一次.

示例：
    const a0 = iota // a0 = 0  // const出现, iota初始化为0

    const (
        a1 = iota   // a1 = 0   // 又一个const出现, iota初始化为0
        a2 = iota   // a1 = 1   // const新增一行, iota 加1
        a3 = 6      // a3 = 6   // 自定义一个常量
        a4          // a4 = 6   // 不赋值就和上一行相同
        a5 = iota   // a5 = 4   // const已经新增了4行, 所以这里是4
    )

几个常见的iota示例:
	使用_跳过某些值：
        const (
                n1 = iota //0
                n2        //1
                _
                n4        //3
            )

	iota声明中间插队：
        const (
                n1 = iota //0
                n2 = 100  //100
                n3 = iota //2
                n4        //3
            )
            const n5 = iota //0

    定义数量级 （这里的<<表示左移操作，1<<10表示将1的二进制表示向左移10位，也就是由1变成了10000000000，也就是十进制的1024。同理2<<2表示将2的二进制表示向左移2位，也就是由10变成了1000，也就是十进制的8。）

    const (
            _  = iota
            KB = 1 &lt;&lt; (10 * iota)
            MB = 1 &lt;&lt; (10 * iota)
            GB = 1 &lt;&lt; (10 * iota)
            TB = 1 &lt;&lt; (10 * iota)
            PB = 1 &lt;&lt; (10 * iota)
        )

    多个iota定义在一行

    const (
            a, b = iota + 1, iota + 2 //1,2
            c, d                      //2,3
            e, f                      //3,4
        )
```

