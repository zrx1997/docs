### 基本数据类型

​		Go语言中有丰富的数据类型，除了基本的整型、浮点型、布尔型、字符串外，还有数组、切片、结构体、函数、map、通道（channel）等。Go 语言的基本类型和其他语言大同小异。



#### 整型

​	整型分为以下两个大类： 

​		按长度分为：int8、int16、int32、int64 

​         对应的无符号整型：uint8、uint16、uint32、uint64

|  类型  |                             描述                             |
| :----: | :----------------------------------------------------------: |
| uint8  |                  无符号 8位整型 (0 到 255)                   |
| uint16 |                 无符号 16位整型 (0 到 65535)                 |
| uint32 |              无符号 32位整型 (0 到 4294967295)               |
| uint64 |         无符号 64位整型 (0 到 18446744073709551615)          |
|  int8  |                 有符号 8位整型 (-128 到 127)                 |
| int16  |              有符号 16位整型 (-32768 到 32767)               |
| int32  |         有符号 32位整型 (-2147483648 到 2147483647)          |
| int64  | 有符号 64位整型 (-9223372036854775808 到 9223372036854775807) |



**特殊整型**

|  类型   |                          描述                          |
| :-----: | :----------------------------------------------------: |
|  uint   | 32位操作系统上就是`uint32`，64位操作系统上就是`uint64` |
|   int   |  32位操作系统上就是`int32`，64位操作系统上就是`int64`  |
| uintptr |              无符号整型，用于存放一个指针              |

```
注意： 
	在使用int和 uint类型时，不能假定它是32位或64位的整型，而是考虑int和uint可能在不同平台上的差异。

	获取对象的长度的内建len()函数返回的长度可以根据不同平台的字节长度进行变化。实际使用中，切片或 map 的元素数量等都可以用int来表示。在涉及到二进制传输、读写文件的结构描述时，为了保持文件的结构不会受到不同编译目标平台字节长度的影响，不要使用int和 uint。
```

 

**数字字面量语法（Number literals syntax）**

```go
	Go1.13版本之后引入了数字字面量语法，这样便于开发者以二进制、八进制或十六进制浮点数的格式定义数字

例如：
	v := 0b00101101， 代表二进制的 101101，相当于十进制的 45。 v := 0o377，代表八进制的 377，相当于十进制的 255。 v := 0x1p-2，代表十六进制的 1 除以 2²，也就是 0.25。 而且还允许我们用 _ 来分隔数字，比如说：
	v := 123_456 等于 123456。


    package main

    import "fmt"

    func main()  {
        // 十进制
        var a int = 10
        fmt.Printf("%d \n", a)
        fmt.Printf("%b \n", a)

        // 八进制  以0开头
        var b int = 077
        fmt.Printf("%o \n", b)

        // 十六进制 以0x开头
        var c int = 0xff
        fmt.Printf("%x \n", c)
        fmt.Printf("%X \n", c)

    }
```



#### 浮点型

```go
Go语言支持两种浮点型数：
    float32
    float64
这两种浮点型数据格式遵循IEEE 754标准： 
    float32 的浮点数的最大范围约为 3.4e38，可以使用常量定义：math.MaxFloat32。 
    float64 的浮点数的最大范围约为 1.8e308，可以使用一个常量定义：math.MaxFloat64。

例如:
	package main

    import (
        "fmt"
        "math"
    )

    func main() {
        fmt.Printf("%f \n", math.Pi)
        fmt.Printf("%2f \n", math.Pi)
    }
```



#### 复数

```go
复数有实部和虚部
	complex64的实部和虚部为32位
	complex128的实部和虚部为64位


package main

import (
	"fmt"
	"math"
)

func main() {
	var c1 complex64
	c1 = 1 +2i

	var c2 complex128
	c2 = 2 + 3i

	fmt.Println(c1)
	fmt.Println(c2)
	fmt.Println("c2")
}

注意：
	go不支持在函数外进行运算


```



#### 布尔值

```GO
Go语言中以bool类型进行声明布尔型数据，布尔型数据只有true（真）和false（假）两个值。

注意：
    布尔类型变量的默认值为false。
    Go 语言中不允许将整型强制转换为布尔型.
    布尔型无法参与数值运算，也无法与其他类型进行转换。
```



#### 字符串

```go
	Go语言中的字符串以原生数据类型出现，使用字符串就像使用其他原生数据类型（int、bool、float32、float64 等）一样。 
	Go 语言里的字符串的内部实现使用UTF-8编码
	字符串的值为双引号("")中的内容，可以在Go语言的源码中直接添加非ASCII码字符

        package main

        import (
            "fmt"
        )

        func main() {
            d1 := "hello"
            d2 := "你好"

            fmt.Println(d1)
            fmt.Println(d2)

        }

多行字符串
	Go语言中要定义一个多行字符串时，就必须使用反引号字符：

        package main

        import (
            "fmt"
        )

        func main() {
            s1 := `第一行\n
            第二行
            第三行`
            fmt.Println(s1)

        }
	反引号间的换行将被作为字符串中的换行，但是所有的转义字符均会无效，文本将会按照原样输出
```

##### **字符串转义符**

​		Go 语言的字符串常见转义符包含回车、换行、单双引号、制表符等，如下表所示。

| 转义符 |                含义                |
| :----: | :--------------------------------: |
|  `\r`  |         回车符（返回行首）         |
|  `\n`  | 换行符（直接跳到下一行的同列位置） |
|  `\t`  |               制表符               |
|  `\'`  |               单引号               |
|  `\"`  |               双引号               |
|  `\\`  |               反斜杠               |

​		例如： 打印Windows文件路径

```go
    package main

    import (
        "fmt"
    )

    func main() {
        fmt.Println("str := \"c:\\Code\\lesson1\\go.exe\"")
    }
```

##### 字符串的常用操作

|                方法                 |      介绍      |
| :---------------------------------: | :------------: |
|              len(str)               |     求长度     |
|           +或fmt.Sprintf            |   拼接字符串   |
|            strings.Split            |      分割      |
|          strings.contains           |  判断是否包含  |
| strings.HasPrefix,strings.HasSuffix | 前缀/后缀判断  |
| strings.Index(),strings.LastIndex() | 子串出现的位置 |
| strings.Join(a[]string, sep string) |    join操作    |

```go
Go 语言的字符有以下两种：
	uint8类型，或者叫 byte 型，代表了ASCII码的一个字符。
	rune类型，代表一个 UTF-8字符。

	当需要处理中文、日文或者其他复合字符时，则需要用到rune类型。rune类型实际是一个int32。
	Go 使用了特殊的 rune 类型来处理 Unicode，让基于 Unicode 的文本处理更为方便，也可以使用 byte 型进行默认字符串处理，性能和扩展性都有照顾。

组成每个字符串的元素叫做“字符”，可以通过遍历或者单个获取字符串元素获得字符。 
字符用单引号（''）包裹起来

1、字符串的切片：
    package main

    import (
        "fmt"
    )

    func main() {
        str := "Hello World!"
        subStr := str[6:11]
        fmt.Println(subStr)
    }

2、判断字符串的长度（字节数）
	str := "Hello World!"
	subStr := len(str)
	fmt.Println(subStr)
	utf8.RuneCountInString(str)	// 等同于len(str)

3、字符串的拼接

    直接用"+="操作符，直接将多个字符串拼接。最直观的方法，不过当数据量非常大时用这种拼接访求是非常低效的。
			str1 := "Hello "
            str2 := "World!"
            ref := str1 + str2 //str1 == "Hello World!"
            fmt.Printf(ref)

    用字符串切片([]string)装载所有要拼接的字符串，最后使用strings.Join()函数一次性将所有字符串拼接起来。在数据量非常大时，这种方法的效率也还可以的。
			

    利用Buffer(Buffer是一个实现了读写方法的可变大小的字节缓冲)，将所有的字符串都写入到一个Buffer变量中，最后再统一输出。






	
```

