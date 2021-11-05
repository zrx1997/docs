# Typescript

英文官网：https://www.typescriptlang.org/

中文官网：https://www.tslang.cn/

## 介绍

![typescript](https://raw.githubusercontent.com/adcwb/storages/master/def439ecb1095195a0ffd963e06d6212.png)

TypeScript 是一种**强类型**的编程语言，它起源于使用JavaScript开发的大型项目，由于JavaScript本身属于**弱类型**语言的局限性，难以胜任和维护大型项目的开发工作。因此微软于2012年推出了TypeScript ，使得其能够胜任开发大型项目。

TypeScript通过在JavaScript的基础上添加静态类型定义构建而成，可以编译为 JavaScript代码来执行。它最大特点是强大的类型系统和对ES6规范的支持，TypeScript托管于GitHub上面。

```
ES6：ECMA2015/2016/2017的简称，刚好是属于ECMA的第6个版本。
javascript：ECMA语法，BOM浏览器对象模型和DOM文档对象模型。js是网景公司推出的浏览器端脚本语言。
欧洲计算机制造协会:简称ECMA
```

### 特点

-   类型系统：类型注解、编译时类型检查、类型推断和类型擦除
-   接口
-   枚举
-   Mixin
-   泛型编程
-   命名空间

从 ECMA 6规范中移植而来的：

-   类
-   模块
-   lambda 函数的箭头语法
-   可选参数以及默认参数
-   元组【事实上就是js里面的数组来的，只是typescript提供了不同的玩法而已，和python里面的元祖不是一回事】
-   await / async



#### JavaScript 与 TypeScript 的关系和区别

​                                   ![img](https://raw.githubusercontent.com/adcwb/storages/master/ts-2020-11-26-2.png)             ![img](assets\ts-2020-11-26-1.png)

TypeScript属于Javascript 的**超集**，扩展了Javascript的语法，现有的Javascript代码可以不经任何改动的情况下在TypeScript环境下运行。同时TypeScript代码，可以通过typescript的编译器转换为纯正的 JavaScript代码，且编译出来的 JavaScript代码能够运行在任何浏览器上。TypeScript 的编译工具也可以运行在任何服务器和任何系统上。

typeScript文件的后缀为.ts。

### 优势

+   现有大部分的流行的代码编辑器IDE工具都支持typescript，在编写typescript代码时，比原生javascript提示更加友好。

    typescript的类型系统相当于最好的文档对于陌生函数或者类的使用更加透明，易懂。

+   typescript提供的类型系统增强了前端代码的可读性和可维护性，在编译时即可提前发现大部分的错误，不需要项目运行即可提前锁定大部分类型相关错误。

+   完全支持 es6 规范，编译过后生成的javascript代码可以在任何浏览器上运行，解决了各个前端浏览器对于es6规范在不同程度上的兼容问题。

+   有活跃的社区，大多数的第三方库都可提供给 ts 的类型定义文件



### 缺点

+   具有一定的学习成本，需要理解接口、泛型编程、枚举类型等一系列概念
+   短期增加开发成本，在原生javascript基础上，多写一些类型的定义.
+   集成到项目构建流程需要一些工作量
+   和一些现有的javascript第三方库或框架的结合存在bug



## 安装

有两种主要的方式来获取TypeScript工具：

-   通过npm（Node.js包管理器）
-   安装Visual Studio的TypeScript插件

在此，我们通过npm来安装/更新typescript

```
# 安装
npm install -g typescript
# 更新到最新版本
npm update -g typescript
# 查看版本
tsc -v
```



## 快速入门

### 创建typescript文件 

main.ts，代码：

```typescript
function main(person) {
    return "Hello, " + person;
}

var user = "Jane User";

document.body.textContent = main(user);
```

### 编译代码

上面代码中，虽然我们创建脚本文件是ts，但是里面的代码却是实实在在的js代码。不过因为基于typescript和javascript的关系，我们可以直接通过typescript编译器进行编译。

main.ts --->编译--> main.js

终端执行：

```bash
tsc main.ts
# tsc --out main.js main.ts  # --out 可以指定编译完成以后的js文件名
```

命令执行以后的输出结果为一个main.js文件，它包含了和输入文件中相同的JavsScript代码。

虽然，在上面过程中，我们并没有接触到typescript代码，但是我们掌握了typescript编译器的用法。有没有？

最后，编译完成以后得到的js文件就可以直接通过script标签被html使用，变相地，等同于typescript被使用了。

index.html，代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- async是javascript在ES6新出的延时加载关键字 -->
    <script async src="main.js"></script>
</head>
<body>
	
</body>
</html>
```



接下来让我们看看TypeScript工具带来的高级功能。

### 类型注解

main.ts，代码中给`main`函数的参数person添加`: string`类型注解，如下：

```typescript
function main(person: string) {
    return "Hello, " + person;
}

let user = "Jane User";

document.body.textContent = main(user);
```

没错，有没有点熟悉的感觉？没错，python3.5以后的版本中也新增了类型注解功能，在新版本的很多python框架里面都存在着类似的代码。

终端执行：

```bash
tsc main.ts
```

尝试把`person`参数的实参改成传入一个数组：

```typescript
function main(person: string) {
    return "Hello, " + person;
}

let user = [0, 1, 2];

document.body.textContent = main(user);
```

重新编译，你会看到产生了一个错误，当然，类似pycharm这样的IDE工具，要已经有错误提示了。

```
error TS2345: Argument of type 'number[]' is not assignable to parameter of type 'string'.
```

![image-20210128030545427](https://raw.githubusercontent.com/adcwb/storages/master/image-20210128030545427.png)

TypeScript告诉你，使用了非期望个数的参数调用了这个函数。在编译过程中，TypeScript提供了静态的代码分析，它可以分析代码结构和提供的类型注解。当然，尽管编译出现了错误，`main.js`文件还是被创建了。 就算你的代码里有错误，你仍然可以使用TypeScript。



## 数据类型

| 数据类型   | 关键字    | 描述                                                         |
| :--------- | :-------- | :----------------------------------------------------------- |
| 任意类型   | any       | 如果不声明类型，默认则声明为 any 的变量可以赋予任意类型的值。 |
| 数值类型   | number    | 等同于JavaScript的number类型，在TypeScript中所有的数字都是浮点数，都是number类型。<br>let num1: number = 0b1010; // 二进制<br>let num2: number = 0o744;    // 八进制<br>let num3: number = 6;    // 十进制 <br>let num4: number = 0xf00d;    // 十六进制<br>**注意：**TypeScript 和 JavaScript 都是没有整型的。 |
| 字符串类型 | string    | 一个字符系列，使用单引号（**'**）或双引号（**"**）来表示字符串类型。反引号（****）来定义多行文本和内嵌表达式。<br/>let name: string = "xiaoming"; <br/>let qq_number: string= '50000000'; <br/>let text: string = \`您好，我叫 \${ name } ，我的QQ号码是${qq_number} `; |
| 布尔类型   | boolean   | 只有2个值：true 和 false。<br/>let sex: boolean = true;      |
| 数组类型   | 无        | 声明变量为数组。<br/>let arr: number[] = [1, 2];            // 在元素类型后面加上[]<br>let arr: Array\<number> = [1, 2]; // 数组泛型 |
| 元组       | 无        | 元组类型用来表示已知元素数量和类型的数组，各元素的类型不必相同，对应位置的类型需要相同。元祖在原生js中本身是支持的。<br>let x: [string, number]; <br>x = ['xiaoming', 16];    // 运行正常 <br/>x = [16, 'xiaoming'];    // 报错 <br/>console.log(x[0]);        // 输出 xiaoming |
| 枚举       | enum      | 枚举类型用于定义数值集合。<br/>enum Color {Red, Green, Blue}; <br/>let c: Color = Color.Blue; <br/>console.log(c);    // 输出 2 |
| void       | void      | 用于标识方法返回值的类型，表示该方法没有返回值。<br/>function hello(): void {    <br/>        alert("Hello xiaoming"); <br/>} |
| null       | null      | 空。                                                         |
| undefined  | undefined | 未定义                                                       |
| never      | never     | never 是其它类型（包括 null 和 undefined）的子类型，代表从不会出现的值。 |

了解了typescript支持的数据类型以后，其实我们可以更加清晰一点就是javascript里面有的，能使用的，typescript就一定有，并也能使用。所以接下来的学习中，针对javascript和typescript存在差异的地方我们进行讲解，而相同的则默认和javascript是一样的。

例如，接下来关于语法中，变量的命名规范，运算符，流程控制语句等等，这些我们就不会提及了。



## 变量

### 变量的声明

```typescript
// 1.声明变量时，直接指定变量的数据类型
var 变量名:类型 = 值;
// 2.不指定类型，默认类型为any
var 变量名 = 值;
// 3.预设变量，指定类型
var 变量名:类型;
// 4.不指定类型和值，默认类型为any, 默认值为 undefined：
var 变量名;
```

在开发中上面4种格式，最常见的是第3种，代码：

```typescript
var username:string = "hello world";
username = "xiaoming";
username = 123;  // error TS2322: Type 'number' is not assignable to type 'string'.
console.log(username);
```



### 变量作用域

变量作用域指代：根据变量定义的位置来决定变量的使用范围和生命周期。

TypeScript提供了三种不同的作用域：

-   **全局作用域**

    全局变量定义在程序结构的外部，它可以在你代码的任何位置使用。

-   **类作用域**

    这个变量也可以称为 **属性**或者**字段**。

    类变量基本声明在类里的头部位置，不但可以在类的方法里面进行调用，也可以在类方法外面，该变量可以通过类名来访问。

    类变量也可以是静态变量，静态变量可以通过类名直接访问。

-   **局部作用域**

    局部变量，局部变量只能在声明它的一个代码块（如：方法）中使用。

```typescript
var global_num = 12          // 全局变量
class Numbers { 
   num_val = 13;             // 实例变量
   static sval = 10;         // 静态变量
   
   storeNum():void { 
      var local_num = 14;    // 局部变量
   } 
} 
console.log("全局变量为: "+global_num)  
console.log(Numbers.sval)   // 静态变量
var obj = new Numbers(); 
console.log("实例变量: "+obj.num_val)
```



### 联合类型

```typescript
// 语法
var 变量 = 类型1|类型2|类型3|...;

// 注意：
// 联合类型（Union Types）可以通过管道(|)将变量设置多种类型，赋值时可以根据设置的类型来赋值。只能赋值指定的类型，如果赋值其它类型就会报错。
```

代码：

```typescript
// 允许变量在使用过程中,值可以是给出的多个类型之一
var age:string|number; // 联合类型的定义

age = 20;
age = "20";

var data:string|number|number[]|string[];  // 4个类型组合,联合类型
data = 12;
console.log("数字为 "+ data);
data = "xiaoming";
console.log("字符串为 " + data);
data = [1,2,3];
console.log("数组为 " + data);
data = ["a","b","c"];
console.log("数组为 " + data);
data = true; // error TS2322: Type 'boolean' is not assignable to type 'string | number | number[]'.
console.log("布尔值为 " + data);
```



## 函数

typescript和javascript在函数的声明以及使用中，出了类型注解以外，并没有其他区别。所以接下来的例子中，仅仅以普通函数作为例子进行讲解，至于匿名函数，箭头函数（lambda函数），闭包函数，则不会提到。

### 函数的声明

```typescript
// 普通函数
function func_name( param1 [:type], param2 [?:type],param3[?]....) [:return_type]{
    
}

// lambda函数
var func = (param1:type) => expression;

/*
 type表示形参的数据类型，可以指定类型，也可以不指定类型
 return_type 表示函数执行以后的返回值的数据类型，可以指定，也可以不指定
 形参后面跟着?，表示当前参数是可选参数，可填可不填
 */
```

代码：

```typescript
// 普通函数的定义
// 参数有3种:
// 必填参数[可以限定类型]
// 可选参数 ?  [可以限定类型]
// 默认参数,提供了默认值,[可以限定类型,即便不限定类型,typescript也会通过默认值进行类型判定]
function func1(arg1,arg2:number,arg3?,arg4?:string,arg5:string="xioaming"):void{
    console.log(`arg1=${arg1},arg2=${arg2},arg3=${arg3},arg4=${arg4},arg5=${arg5}`);
}
// javasctipt/typescript在读取代码的时候,分2遍的
// 从上到下,进行词法检测,识别关键字,分配空间[]
// 从上到下,进行代码执行
func1(100,200);

// 此处arg5导致报错,是因为typescript内置的类型系统包含了类型的判断,
// 在函数声明时的参数列表中,已经对arg5进行默认值的分配,因为这个默认值的原因,
// 所以typescript根据arg5的默认值进行了类型判断,识别到了是string,
// 因此,在调用函数时传递的参数是number就肯定报错了
// func1(100,200,300,"400",500);


// 类型判定
// var data = "数据";
// data = 200;

// 箭头函数
// var func = (num1:number,num2:number):number => {return num1+num2}; // 原生script的写法
var func = (num1:number,num2:number):number => num1+num2; // typescript允许出现表达式
console.log( func(100,200) );
```



### 函数重载

错误写法：

```typescript
function func1(str1:string):void{
    console.log(str1);
}

function func1(num1:any,str1?:any):void {
    console.log(num1);
    console.log(str1);
}
func1("hello");
func1(16,"hello");
```

正确写法：

```typescript
function func1(str1:string):void;
function func1(num1:number,str1:string):void;

function func1(num1:any,str1?:string):void {
    console.log(num1);
    console.log(str1);
}
func1("hello");
func1(16,"hello");
```



## 类

### 类的声明和使用

```typescript
class Humen {
   age:number;
   desc():string {
       return `我今年${this.age}岁`;
   }
   constructor(age:number) {
      this.age = age
   }
}

// 继承
class Person extends Humen {
   desc():string {
        return "您好，"+super.desc();
   }
}

var people = new Person(13);
console.log( people.desc() );
```

### 静态属性和方法

```typescript
class Static {
   // 静态属性
   static num:number;
   // 静态方法
   static desc():void {
      console.log("num 值为 "+ Static.num)
   }
}

Static.num = 12;     // 初始化静态属性/变量
Static.desc();       // 调用静态方法
```

### 访问控制符

面向对象中的所谓封装，本质上就是把一系列相关的数据(属性/变量/字段)和操作数据的方法(方法/函数)集中到一个数据结构中(类)，达到隐藏数据和操作数据的方法，对外暴露有限的操作数据方法。

TypeScript 中，可以使用访问控制符来保护对类、变量、方法和构造方法的访问。TypeScript 支持 3 种不同的访问权限。\

-   **public（默认）** : 公有的，可以在任何地方被访问。
-   **protected** : 受保护，可以被其自身以及其子类和父类访问。
-   **private** : 私有，只能被其定义所在的类访问。

代码：

```typescript
// 公有属性: 允许任何一个地方调用
// 私有属性: 仅允许当前类内部进行调用
// 保护属性: 仅允许当前类或直接间接继承了当前类的子类内部进行调用
class Proto{
   public desc(){                   // 公有方法
      return `我住在树上`;
   }
}
class Humen extends Proto{
   public address:string = "北京市"; // 公有属性
   public desc(){                   // 公有方法
      return `我住在${this.address}`;
   }

   private money:number = 10000;    // 私有属性
   private calc_money(){
      return this.money*0.1;  // 类的内部才可以调用私有属性,私有方法
   }
   // 如果允许私有属性提供给外界查看, 往往通过公有方法来进行暴露
   public show_money(){
      return this.calc_money();
   }

   protected phone:string = "13300000000";  // 保护属性
   protected get_phone(){                   // 保护方法
      return `我的手机号码:${this.phone}`; // 类的内部或者子类才可以调用保护属性/方法
   }
   // 如果允许保护属性提供给外界查看,往往通过公有方法来进行暴露
   public show_phone(key?){
      if(key == "123456"){
         return this.get_phone();
      }
   }
}

class People extends Humen{
   public show_father_data(){
      // return this.phone;    // 调用了父类的保护属性
      // return this.get_phone(); // 调用了父类的保护方法

      // return this.money;       // 子类无法调用父类的私有属性或方法

      // return this.desc();  // 调用继承到的父类方法或者属性,如果当前类重载了则出现覆盖
      return super.desc();
   }

   public desc(){
      return `您好, 我住在${this.address}`;
   }

}

var xiaoming = new People();
// console.log(xiaoming.address);
// console.log(xiaoming.desc());
// console.log(xiaoming.show_money());
// console.log(xiaoming.show_phone());
// console.log(xiaoming.show_phone(123456));
console.log(xiaoming.show_father_data());
```



## 接口

接口(interface)是一系列抽象属性和方法的集合声明，这些方法都应该是抽象的，需要由具体的类去实现，然后外界就可以通过这组抽象方法调用，让具体的类执行具体的方法。

**接口的作用在开发中针对的是数据对象和类的结构进行描述和规范化。**说白了，就是你老大叫你声明一个类/对象，但是这个类/对象长什么样？他会以接口的格式先定义好，然后你照着这个接口定义好的格式进行编写一个类/对象出来，免得你弄乱结构，以后没法复用代码。

一般只有在中大型项目，或者框架/大型模块中为了更好的组织代码结构才会出现抽象类/接口

### 定义接口

```typescript
interface interface_name {
    field: string, 
    func: ()=>string  // 限定了方法名，和返回值
}
```

### 接口的声明和实现

```typescript
interface Person {
    username: string;            // 接口属性，仅仅定了属性名，属性值和属性的初始化，都是在类中完成的
    age: number;
    desc(user: string): string;  // 接口方法，仅仅定义了方法名，参数以及返回值，具体的方法代码是在类中实现的
}

class Humen implements Person {
  username: string;
  age:number;
  desc(user:string){
      return `你好!${user}，我叫${this.username}，我今年${this.age}岁．`;
  }
  constructor(username: string, age: number) {
  	this.username=username;
  	this.age=age;
  }
}

var xiaohong = new Humen("小红",15);
console.log(xiaohong.desc("小白"));
```

>   凡是实现(implements)了接口/抽象类的类, 都要和接口/抽象类保持拥有一样的属性和方法

#### 接口的使用

typescript允许直通过对象来直接实现接口,跳过了类的实现过程

```python
interface Person {
    username: string;
    age: number;
    desc():string
}

function main(person: Person) {
    return "Hello, 我叫" + person.username + "，我今年" + person.age+"岁.";
}

// typescript允许直通过对象来直接实现接口,跳过了类的实现过程
// var 对象名 = <接口名称>{
//    属性;
//    方法;
// }
let user = <Person>{
   username: "小白",
   age: 16,
   desc(){
      return "hello"
   }
};
console.log(main(user));
// js就是披着面向对象外壳的函数式编程语言
```

#### 鸭子类型

在传递实例参数时，不管当前传入的实例参数是否是限定的类/接口的实例对象，只要有同样的属性/方法，那么我们就认为当前实例参数就是这个限定类/接口的实例对象。这就是所谓的**鸭子类型**。

```typescript
// 鸭子类型:
// 一个对象有效的语义，不是由继承自特定的类或实现特定的接口，
// 而是由"当前方法和属性的集合"决定

interface Person {
    username: string;
    age: number;
}

function main(person: Person) {
    return "Hello, 我叫" + person.username + "，我今年" + person.age+"岁.";
}

var xm = {username:"小明",age:20}; // 问题来了,这里明明没有实现Person接口,为什么也能调用
console.log(main(xm));
```



##### python中的鸭子类型

```python
class Person(object):
    def __init__(self,username,age):
        self.username = username
        self.age = age

class Humen(object):
    def __init__(self,username,age):
        self.username = username
        self.age = age

def main(obj:Person):
    return "我叫%s,我今年%s岁了" % (obj.username,obj.age)

if __name__ == '__main__':
    p1 = Person("小明", 15)
    p2 = Humen("小白", 15)
    print( main(p2) )
```



### 接口继承

#### 单继承

```typescript
interface Person {
   age:number
}

interface Humen extends Person {
   username:string
   desc(user:string):string
}

class People implements Humen{
   age:number;
   username:string;
   constructor(){

   }
   init(username,age){
      this.age = age;
      this.username=username;
   }
   desc(user:string):string{
      return `${user},您好!我叫${this.username},我今年${this.age}岁.`
   }
}

var xm = new People();
console.log( xm.desc("小红") );
```

#### 多继承

```typescript
interface Person {
   age:number
}

interface Humen {
   username:string
}

interface People extends Person, Humen {
   // 子接口也可以有自己的接口属性和方法

}

class Student implements People{
   age:number;
   username:string;
   desc(user:string){
      return `你好!${user}，我叫${this.username}，我今年${this.age}岁．`;
   }
   constructor(username: string, age: number) {
    this.username=username;
    this.age=age;
   }
}

var xm = new Student("小白",15);
console.log(xm.desc("小黑"));
```



## 抽象类

抽象类（abstract class）做为其它派生类的基类使用。 它们一般不会直接被实例化。 不同于接口，抽象类可以包含成员的实现细节。 `abstract`关键字是用于定义抽象类和在抽象类内部定义抽象方法。

代码：

```typescript
// 抽象父类
abstract class Animal{
    abstract makeSound(): void;        // 抽象方法，没有函数体
    constructor(public name: string){  // 抽象类的构造方法

    }
    desc(): void {   // 抽象类中也可以定义子类的公共方法或公共属性
        console.log('roaming the earch...');
    }
}

// 抽象子类
abstract class Dog extends Animal{
    abstract move(): string;
}

// 具象类/具体类
class ChineseGardenDog extends Dog{
    public name:string;
    makeSound(){
        return "汪汪汪~"
    }
    move(): string {
        return "奔跑中...."
    }
    constructor(name: string){
        super(name); // 继承了抽象类的子类,必须对父类进行初始化
    }
}

var dog = new ChineseGardenDog("来福");
console.log(dog.name);
console.log(dog.makeSound());
```



## 装饰器

随着TypeScript和ES6里引入了类，在一些场景下我们需要额外的特性来支持标注或修改类及其成员。 装饰器（Decorators）为我们在类的声明及成员上通过元编程语法添加标注提供了一种方式。装饰器是一种特殊类型的声明，它能够被附加到[类声明](https://www.tslang.cn/docs/handbook/decorators.html#class-decorators)，[方法](https://www.tslang.cn/docs/handbook/decorators.html#method-decorators)， [访问符](https://www.tslang.cn/docs/handbook/decorators.html#accessor-decorators)，[属性](https://www.tslang.cn/docs/handbook/decorators.html#property-decorators)或[参数](https://www.tslang.cn/docs/handbook/decorators.html#parameter-decorators)上。

代码：

```typescript
function derator1() {
    console.log("derator1(): evaluated");
    return function (target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log("derator1(): called");
    }
}

function derator2(name:string) {
    console.log(`derator2(): evaluated,name=${name}`);
    return function (target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log(`derator2(): called,name=${name}`);
    }
}

class Demo {
    @derator1()
    @derator2("xiaoming")
    show() {
        console.log("show()执行了")
    }
}

var d = new Demo();
d.show();

/*
 * 输出结果顺序:
 * derator1(): evaluated
 * derator2(): evaluated,name=xiaoming
 * derator2(): called,name=xiaoming
 * derator1(): called
 * show()执行了
 *
 */
```



## 命名空间

当项目大了以后，需要创建和声明的函数，类就多了，自然人也就多了，人多就坏事。想想全国有几个张三？

命名空间（namespace）一个最明确的目的就是解决重名问题。

命名空间定义了标识符的可见范围，一个标识符可在多个名字空间中定义，它在不同名字空间中的含义是互不相干的。这样，在一个新的名字空间中可定义任何标识符，它们不会与任何已有的标识符发生冲突，因为已有的定义都处于其他名字空间中。

### 定义命名空间

app.ts，代码：

```typescript
// 命名空间的名称采用驼峰式写法
namespace App{ 
    // 需要在命名空间外部可以调用 当前命名空间的类,函数和接口等，则需要在左边添加 export 关键字。
    // 变量
    export var username:string="App空间的变量";
    // 常量,一旦定义以后,不能修改值
    export const NAME = "App命名空间的常量";
    // 函数
    export function func(){
        return "App命名空间里面的func"
    }
    // 类
    export class Humen{

    }
    // 当然，在当前命名空间下也是可以执行代码的    
}

```

### 导入命名空间

main.ts，代码：

导入其他命名空间的格式：`/// <reference path = "文件名" />`，可以导入多个命名空间，一行一个。

```typescript
/// <reference path="app.ts" />
console.log(App.func());  // 调用其他命名空间的内容，必须以"命名空间的名称.xxxx"格式进行调用
console.log(App.NAME);
console.log(App.username);
console.log(new App.Humen());
```

使用了命名空间以后，编译命令需要稍微调整如下：

```bash
tsc --out main.js main.ts  # 必须指定--out参数才能正常编译
```



## 模块

TypeScript 模块的设计理念是可以更换的组织代码。模块是在其自身的作用域里执行，并不是在全局作用域，这意味着定义在模块里面的变量、函数和类等在模块外部是不可见的。

typescript提供了两种模块：**内部模块**和**外部模块**，因为外部模块需要依赖第三方框架才可以使用，例如：commonjs，requirejs等。所以在此，我们只简单介绍内部模块的声明和使用。

### 内部模块

#### 声明模块

app.ts，代码：

```typescript
module App{
    export class Humen {
        desc(){
            console.log("hello");
        }
    }

    export function func(){
        console.log("hello, func");
    }

}
```

#### 调用模块

main.ts，代码：

```typescript
module App{ // 模块名称,采用大驼峰写法
    // 允许其他模块调用当前模块的内容,则还是使用export暴露出去
    export class Humen {
        desc(){
            console.log("hello,Humen.desc");
        }
    }

    export function func(){
        console.log("hello, func");
    }

}
```

使用了内部模块以后，编译命令和命名空间一样：

```
tsc --out main.js main.ts
```

### 外部模块

Out.ts，代码：

```typescript
class Humen{
    uname:string;
    constructor(uname){
        this.uname = uname;
    }
    desc() {
        return `您好,我叫 ${this.uname}`;
    }
}
export { Humen };
export { Humen as People };
```

导入模块，main.ts，代码：

```typescript
import { Humen, People } from "./Out";

let obj1 = new Humen("小白");
let obj2 = new People("小黑");
obj1.desc();
obj2.desc();
```

编译命令：

```bash
tsc --module es6 main.ts   # --module 表示代码中编写模块的规范和标准
```



## 编译配置文件

基于typescript开发的项目根目录，一般都会存在一个文件，叫**tsconfig**。这是typescript的编译配置文件。

配置选项：https://www.tslang.cn/docs/handbook/compiler-options.html

tsconfig.json，常用配置项说明，代码：

```json
// 当前配置文件名必须固定是: tsconfig.json
// 同时,json文件中不能出现注释的,所以此处的注释仅仅是为了学习,开发中决不能有
{
    "compilerOptions": {
        "module": "system",     // 项目中编写模块的规范标准
        "noImplicitAny": true,  // 表达式或声明上有隐含的 any类型时报错
        "removeComments": true, // 删除所有注释，除了以 /!*开头的版权信息。
        "preserveConstEnums": true,  // 保留const和Enums声明
        "outDir": "script",  // 编译结果保存目录
        // "outFile": "../../built/local/tsc.js",  // 编译以后输出的文件,一般用不上
        "sourceMap": true,  // 生成相应的 .map文件
        "experimentalDecorators": true,  // 启用实验性的ES装饰器
        "lib": [ // 编译过程中需要引入的库文件的列表
            "es5",
            "dom",
            "es2015.promise"
        ]
    },
    "files": [   // 指定要编译的文件列表, 与include和exclude冲突,开发中,一般使用exclude
      "main.ts"
    ]
  //    "include": [ // 指定要编译的文件所在目录
////        "src/**/*",
//        "./"
//    ],
//    "exclude": [ // 指定在编译时排除的文件目录
//        "node_modules",
//        "**/*.spec.ts"
//    ]
}
```





# Python的类型注解

## typing模块

自python3.5开始，PEP484为python引入了类型注解(type hints)

-   类型检查，防止运行时出现参数和返回值类型、变量类型不符合。

-   作为开发文档附加说明，方便使用者调用时传入和返回参数类型。

-   该模块加入后并不会影响程序的运行，不会报正式的错误，只有提醒。

    pycharm目前支持typing检查，参数类型错误会黄色提示。

## 常用类型

-   int,long,float: 整型,长整形,浮点型
-   bool,str: 布尔型，字符串类型
-   List, Tuple, Dict, Set:列表，元组，字典, 集合
-   Iterable,Iterator:可迭代类型，迭代器类型
-   Generator：生成器类型

## 基本类型指定

代码：

```python

from typing import List,Dict,Tuple,Union
# 整型
num:int = 100
# 字符串
data:str = "200"
# 布尔值
bo:bool = True
# 列表
data_list:List[str] = ["1","2","3"]
# 字典
data_dict:Dict[str, str] = {"name":"xiaoming",}
# 元组[限制数据和类型]
data_tuple:Tuple[int,int,bool] = (1,2,False)

# 联合类型[泛型]
U1 = Union[str,int] # 只能是字符串或者整形
data_union1:U1 = "20"
data_union2:U1 = 200
data_union3:U1 = [1,2,3]  # 此处不符合要求,出现黄色提示

def test(a:int, b:str) -> str:
    print(a, b)
    return 1000

if __name__ == '__main__':
    test('test', 'abc')

"""
函数test，
a:int  指定了输入参数a为int类型，
b:str  b为str类型，
-> str  返回值为srt类型。

可以看到，
在方法中，我们最终返回了一个int，此时pycharm就会有警告；
当我们在调用这个方法时，参数a我们输入的是字符串，此时也会有警告；
但非常重要的一点是，pycharm只是提出了警告，但实际上运行是不会报错，毕竟python的本质还是动态语言
"""
```



## 复杂的类型标注

代码：

```python
from typing import List
Vector = List[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

# 类型判定: 传递进行的数据只要类似Vector格式即可，这里也是鸭子类型所导致的.
new_vector = scale(2.0, [1.0, -4.2, 5.4])
```

代码：

```python
from typing import Dict, Tuple, Sequence

ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]

def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    ...

# The static type checker will treat the previous type signature as
# being exactly equivalent to this one.
def broadcast_message(
    message: str,
    servers: Sequence[Tuple[Tuple[str, int], Dict[str, str]]]) -> None:
    ...
):
    ...
"""
这里需要注意，元组这个类型是比较特殊的，因为它是不可变的。
所以，当我们指定Tuple[str, str]时，就只能传入长度为2，
并且元组中的所有元素都是str类型
"""
```



## 泛型指定

代码：

```python
from typing import Sequence, TypeVar

T = TypeVar('T')      # 定义泛型变量,可以是任意类型的数据
b2:T = True # b2的值可以是任意类型数据

def first(l: Sequence[T]) -> T:   # Generic function
    return l[0]

A = TypeVar('A', bool, str, bytes)  # 定义当前泛型的范围只能是字符串或者bytes类型
b3:A = "hello"
b4:A = "hello".encode()
b5:A = True
```

## 创建变量时的类型指定

代码：

```python
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    id: int = 3

employee = Employee('Guido')
assert employee.id == 3
```

## 不足之处：提示错误而不影响执行

代码：

```python
from typing import List

def test(b: List[int]) -> str:
    print(b)
    return 'test'


if __name__ == '__main__':
    test([1, 'a'])

"""
从这个例子可以看出来，虽然我们指定了List[int]即由int组成的列表，
但是，实际中，只要这个列表中存在nt（其他的可以为任何类型），就不会出现警告
"""
```