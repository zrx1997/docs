### 一、Vue入门简介

1.1 Vue的安装

```vue

	vue.js是目前前端web开发最流行的工具库，由尤雨溪在2014年2月发布的。
	另外几个常见的工具库：react.js /angular.js/jQuery

官方网站：
	中文：https://cn.vuejs.org/
	英文：https://vuejs.org/
官方文档：https://cn.vuejs.org/v2/guide/

vue.js目前有1.x、2.x和3.x 版本，我们学习2.x版本的。
jQuery和vue的定位是不一样的。
    jQuery的定位是获取元素和完成特效。
    vue的定位是方便操作和控制数据和完成特效。
```





```vue
三个项目：
	1、django+vue+drf开发一个资讯项目
	2、flask+APICloud完成一个手机APP
	3、django+drf+微信小程序开发小程序


	

VUE的两种引入方式
	脚本化引入
	组件化开发
VUE发行版本
	
	
VUE使用的三个步骤
	1、先引入vue核心文件
	2、对vue进行一个实例化
		先声明一个唯一变量
		直接引用vue对象
			el：vue要操作的元素(选择符)，el=elment，表示元素
			data：{保存一些前端使用的数据，键值对方式}
	3、在el属性对应的标签中填写正确的vue语法，展示或者控制数据
Vue对象命名规范：
	遵从js对象的变量命名要求

两种框架的定位
	jQuery主要在于完成特效和获取元素上面
	vue主要是方便我们操作和控制数据上面，也可以完成特效
	
VUE的三个注意项：
	1、1个网页中可以实例化多个vue对象，每个vue对象之间是独立，互不冲突的
	2、js里面的所有变量和语法都是区分大小写的，Vue
	3、实例化的代码不可以乱写，建议实例化vue的代码写在body的最后面， 免得出现HTML元素无法获取的错误

Vue的框架思想
	MVVM；双向数据绑定

在视图模板中显示数据的三种方式：******
	$表示vm对象的属性，这些属性都是vm对象初始化的时候进行赋值的。
	1、v-model
	
Vue对象提供的属性功能
过滤器：
	全局过滤器：
        Vue.filter("format",function(money){
            return money.toFixed(2)+"元"; // js中提供了一个toFixed方法可以保留2位小鼠
        });
		format：过滤器名
		function(money)：用一个function来接收一个参数，之后再将接收到的参数格式化为想要的数据结果
		
	局部过滤器：
        filters: {
          format(money){
                    return money.toFixed(2)+"元";
                }
        }
当全局过滤器和局部过滤器重名时，会采用局部过滤器

	计算属性：
		computed:{
 methods:{}, // vm的方法
            computed:{  // 计算属性，相当于创建一个新的变量保存数据计算的结果
                total(){
                    // parseFloat 把数据转换成浮点数
                    // parseInt   把数据转换成整数
                    return parseFloat(this.num1)+parseFloat(this.num2);
                }

}

	侦听属性：
		watch: {
            num(v1,v2){
                if (this.num >=5){
                    this.num = 5;
                }
                console.log(this.num,v1,v2)
            }
        }

	beforeCreate
		vm初始化完成之前自动执行的代码
	created
		vm初始化完成之后自动执行的代码
	beforeMount
		vm数据渲染到html之前的数据
	mounted
		vm数据渲染到html之后的数据
	beforeUpdate
		数据修改前的操作
	updated
		数据修改之后的操作
	beforeDestroy
		vm对象销毁之前的操作
	destroyed
		vm对象销毁之后的数据
	errorCaptured
		https://cn.vuejs.org/v2/api/#errorCaptured

	事件冒泡：

js中追加一个列表成员使用push

splice高阶函数，可以指定从指定的下标位置开始删除成员的个数
```

