### Angular 简介

```html
	Angular 是谷歌开发的一款开源的web 前端框架，诞生于2009 年，由Misko Hevery 等人创建，后为Google所收购。是一款优秀的前端JS 框架，已经被用于Google 的多款产品当中。

	根据项目数统计angular（1.x 、2.x 、4.x、5.x、6.x、7.x 、8.x、9.x）是现在网上使用量最大的框架。
	Angular 基于TypeScript 和react、vue 相比Angular 更适合中大型企业级项目。

	根据官方介绍，Angular 每过几个月就会更新一个版本。Angular2.x 以后所有的Angular版本用法都是一样的，
```



### 环境准备

```html
1、安装node.js
	https://nodejs.org/zh-cn/download/

2、国内用户可使用cnpm，若网络状态良好，则直接使用node.js自带的npm即可
	npm install -g cnpm --registry=https://registry.npm.taobao.org

3、安装angular脚手架
	npm install -g @angular/cli
	或者 yarn global add @angular/cli
 	i 等同于 install

```



### 项目创建

```html
创建项目：
	ng new 项目名称
		例： ng new angular-web
		注： 项目名不支持_, 其他特殊符号暂未尝试
		--skip-install	跳过安装依赖文件

运行项目：
	cd 项目路径
	ng serve --open
		--open： 自动打开默认的浏览器

创建组件：
	ng g component 组件名
		例： ng g component components/header
		组件名可以跟路径，不存在时会自动创建，创建的组件路径在src目录下

```



- 安装

![image-20210826102750335](https://raw.githubusercontent.com/adcwb/storages/master/image-20210826102750335.png)



```bash
# 项目安装
adcwb@adcwb:~/Projects/angular$ ng new angular-test
? Would you like to add Angular routing? No		    # 是否安装路由，默认回车不安装
? Which stylesheet format would you like to use? 	# 选择样式类型
❯ CSS 
  SCSS   [ https://sass-lang.com/documentation/syntax#scss                ] 
  Sass   [ https://sass-lang.com/documentation/syntax#the-indented-syntax ] 
  Less   [ http://lesscss.org                                             ] 


# 项目结构
adcwb@adcwb:~/Projects/angular/angular-test$ tree 
.
├── e2e					# 端到端测试
├── node_modules		# 项目安装的第三方模块包存放位置
├── angular.json		# angular命令行工具的配置文件
├── karma.conf.js		# karma单元测试配置
├── package.json		# npm安装包配置
├── package-lock.json	# 在 npm install时候生成一份文件，用以记录当前状态下实际安装的各个npm package的具体来源和版本号。如果已经存在 package-lock.json 文件，则它只会根据 package-lock.json 文件指定的结构来下载模块，并不会理会 package.json 文件。

├── README.md			# 项目描述文件
├── src					# 项目开发目录
│   ├── app				# 默认组件
│   │   ├── app.component.css
│   │   ├── app.component.html
│   │   ├── app.component.spec.ts
│   │   ├── app.component.ts
│   │   └── app.module.ts	# 根模块配置文件
│   ├── assets			# 静态资源目录
│   ├── environments	# 此文件夹包括为各个目标环境准备的文件，如开发环境，测试环境，生产环境等
│   │   ├── environment.prod.ts
│   │   └── environment.ts
│   ├── favicon.ico		# 浏览器图标文件
│   ├── index.html		# 入口文件，主页面
│   ├── main.ts			# 应用主要入口文件
│   ├── polyfills.ts	# 填充库，目录环境配置
│   ├── styles.css		# 全局样式
│   └── test.ts			# 单元测试入口文件
├── tsconfig.app.json
├── tsconfig.json		# TypeScript编译器配置文件
└── tsconfig.spec.json
```



- app.module.ts

```typescript
	定义AppModule，这个根模块会告诉Angular如何组装该应用。
    在项目刚创建的时候，它只会声明了AppComponent。也就是根模块
    Angular根模块类描述应用的部件是如何组合在一起的，每个应用都至少有一个angular模块，也就是根模块，用来引导并运行应用，常规名字是AppModule，也就是app.module.ts


// BrowserModule，浏览器解析的模块
import { BrowserModule } from '@angular/platform-browser';  
// Angular核心模块
import { NgModule } from '@angular/core';
// 根组件
import { AppComponent } from './app.component';

// 自定义组件
import { NewsComponent } from './components/news/news.component';
import { HomeComponent } from './components/home/home.component';
import { HeaderComponent } from './components/header/header.component';

/*@NgModule装饰器, @NgModule接受一个元数据对象，告诉 Angular 如何编译和启动应用*/
@NgModule({
  declarations: [    /*配置当前项目运行的的组件*/
    AppComponent, NewsComponent, HomeComponent, HeaderComponent
  ],
  imports: [  /*配置当前模块运行依赖的其他模块*/
    BrowserModule
  ],
  providers: [],  /*配置项目所需要的服务*/
  bootstrap: [AppComponent]    /* 指定应用的主视图（称为根组件） 通过引导根AppModule来启动应用  ，这里一般写的是根组件*/
})

//根模块不需要导出任何东西，   因为其它组件不需要导入根模块
export class AppModule { }

```



- 自定义组件

![image-20210826113943732](https://raw.githubusercontent.com/adcwb/storages/master/image-20210826113943732.png)



```typescript
/* 
	自定义组件详解
	header.component.ts
*/

/* 引入angular核心 */
import { Component, OnInit } from '@angular/core';

/* */
@Component({
  selector: 'app-header',					/* 组件名称 */
  templateUrl: './header.component.html',	/* HTML模板 */
  styleUrls: ['./header.component.css']	    /* css样式 */
})
export class HeaderComponent implements OnInit {
  
  constructor() { /* 构造函数 */ }

  ngOnInit() {		/* 初始化加载的生命周期函数 */
  }

}

```



### 数据绑定

​		Angular 中使用{{}}绑定业务逻辑里面定义的数据

```typescript
// 可以在header.component.ts文件中的export部分声明变量，然后再HTML文件中直接使用jinja2模板语法即可

export class NewsComponent implements OnInit {

  public title="我是一个新闻组件--ts";

  constructor() { }

  ngOnInit() { }

}

// html

<h1>
	{{title}}
</h1>
```

