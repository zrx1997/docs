### Vue的基本使用

```vue
<script>
	// vue.js的代码开始于一个Vue对象。所以每次操作数据都要声明Vue对象开始。
    let vm = new Vue({
    	el:'#app',   // 设置当前vue对象要控制的标签范围。
        
   data属性写法方式1
        data:{  // data是将要展示到HTML标签元素中的数据。
          message: 'hello world!',
        }
    data属性写法方式2:
        data:function () {
         return {
           'msg':'掀起你的盖头来1！'
        	}
        }
	data属性写法方式3:
        data(){   // 单体模式  这种写法用的居多，并且后面学习中有个地方一定要这样写，所以我们就记下来这种写法就可以了
              return {
                  'msg':'掀起你的盖头来2！',
              }
          }
    });
    
</script>
```



### 总结：

```vue
1. vue的使用要从创建Vue对象开始
   var vm = new Vue();
   
2. 创建vue对象的时候，需要传递参数，是自定义对象，自定义对象对象必须至少有两个属性成员
   var vm = new Vue({
     el:"#app",
	 data: {
         数据变量:"变量值",
         数据变量:"变量值",
         数据变量:"变量值",
     },
   });
   
   el:圈地，划地盘，设置vue可以操作的html内容范围，值就是css的id选择器,其他选择器也可以，但是多用id选择器。
   data: 保存vue.js中要显示到html页面的数据。
   
3. vue.js要控制器的内容外围，必须先通过id来设置。
      <div id="app">
          <h1>{{message}}</h1>
          <p>{{message}}</p>
      </div>
```

vue中的变量可以直接进行一些简单直接的js操作

```vue
模板：
	<h2>{{ msg }}</h2> 					<!--vue的模板语法，和django的模板语法类似-->
	<h2>{{ 'hello beautiful girl!' }}</h2>  	<!-- 直接放一个字符串 -->
    <h2>{{ num+1 }}</h2>  				<!-- 四则运算 -->
  	<h2>{{ 2+1 }}</h2>  				<!-- 四则运算 -->
    <h2>{{ {'name':'chao'} }}</h2> 		<!-- 直接放一个自定义对象 -->
    <h2>{{ person.name }}</h2>  <!-- 下面data属性里面的person属性中的name属性的值 -->
    <h2>{{ 1>2?'真的':'假的' }}</h2>  	<!-- js的三元运算 -->
    <h2>{{ msg2.split('').reverse().join('') }}</h2>  <!-- 字符串反转 -->



	<script src="vue.js"></script>
    <script>
    //2.实例化对象
        new Vue({
            el:'#app',
            data:{
                msg:'黄瓜',
                person:{
                    name:'超',
                },
                msg2:'hello Vue',
                num:10,
            }
        })
    </script>
```

### vue.js的M-V-VM思想

MVVM 是Model-View-ViewModel 的缩写，它是一种基于前端开发的架构模式。

`Model` 指代的就是vue对象的data属性里面的数据。这里的数据要显示到页面中。

`View`  指代的就是vue中数据要显示的HTML页面，在vue中，也称之为“视图模板” 。

`ViewModel ` 指代的是vue.js中我们编写代码时的vm对象了，它是vue.js的核心，负责连接 View 和 Model，保证视图和数据的一致性，所以前面代码中，data里面的数据被显示中p标签中就是vm对象自动完成的。



总结

```vue
1. 如果要输出data里面的数据作为普通标签的内容，需要使用{{  }}
   用法：
      vue对象的data属性：
          data:{
            name:"小明",
          }
      标签元素：
      		<h1>{{ name }}</h1>
2. 如果要输出data里面的数据作为表单元素的值，需要使用vue.js提供的元素属性v-model
   用法：
      vue对象的data属性：
          data:{
            name:"小明",
          }
      表单元素：
      		<input v-model="name">
      
   使用v-model把data里面的数据显示到表单元素以后，一旦用户修改表单元素的值，则data里面对应数据的值也会随之发生改变，甚至，页面中凡是使用了这个数据都会发生变化。
```



### Vue指令系统常用指令

```vue
v-text：
```

