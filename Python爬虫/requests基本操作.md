#### requests基本操作



```Python
requests作用：
	就是一个基于网络请求的模块，可以用来模拟浏览器发请求。
    
requests安装：
	工具默认没有集成该模块，需要手动安装
	pip3 install requests

requests模块的使用流程
    - 指定一个字符串形式url
    - 发起请求
    - 获取响应数据
    - 持久化存储

```



#### requests常用参数

```python
requests常用方法：
    requests.request() 构造一个请求，支撑以下各方法的基础方法
    requests.get() 获取HTML网页的主要方法，对应于HTTP的GET
    requests.head() 获取HTML网页头信息的方法，对应于HTTP的HEAD
    requests.post() 向HTML网页提交POST请求的方法，对应于HTTP的POST
    requests.put() 向HTML网页提交PUT请求的方法，对应于HTTP的PUT
    requests.patch() 向HTML网页提交局部修改请求，对应于HTTP的PATCH
    requests.delete() 向HTML页面提交删除请求，对应于HTTP的DELETE

    
requests.get(url, params=None, **kwargs)
	url : 拟获取页面的url链接
	params : url中的额外参数，字典或字节流格式，可选
	**kwargs: 12个控制访问的参数
	构造一个向服务器请求资源的Request对象
	返回一个包含服务器资源的Response对象

Response对象属性
    status_code HTTP请求的返回状态，200表示连接成功，404表示失败
    text HTTP响应内容的字符串形式，即，url对应的页面内容
    encoding 从HTTP header中猜测的响应内容编码方式
    apparent_encoding 从内容中分析出的响应内容编码方式（备选编码方式）
    content HTTP响应内容的二进制形式
    
```



#### https的加密方式：

- https://www.cnblogs.com/wupeiqi/articles/11647089.html

- https是基于http和ssl/tls实现的一个协议，他可以保证在网络上的数据都是加密的，从而保证数据安全
- 在https出现之前，http协议是不安全的，在http协议传输的过程中都是明文传输，存在数据泄露和篡改
- CA证书的应用
    - 使用CA证书可以解决黑客劫持的问题![img](https://raw.githubusercontent.com/adcwb/storages/master/425762-20191012103813623-466756626.png)
    - 注意：https是基于SSL/TLS实现的一个协议，其中前9步称为SSL/TLS过程，之后的传输就是利用http协议进行收发数据

#### 反爬策略 --- UA检测

```python
UA检测
	当次的请求被搜狗认定为是一个异常的请求
	什么是异常的请求？
		服务器端检测到该次请求不是基于浏览器访问。使用爬虫程序发起的请求就是异常的请求。
        
User-Agent：
	本身是请求头中的一个信息。
	概念：请求载体的身份标识
		请求载体：浏览器，爬虫程序
        
反爬机制：UA检测
	对方服务器端会检测请求载体的身份标识，如果不是基于某一款浏览器的身份标识则认定为是一个异常请求，则不会响应会正常的数据。
    
反反爬策略：UA伪装
	将爬虫程序发起的异常的请求载体标识伪装或者修改成某一款浏览器的身份标识即可
 
打开浏览器调试模式---Network---Headers---Request Headers
```

![image-20200807203913575](https://raw.githubusercontent.com/adcwb/storages/master/image-20200807203913575.png)





#### 案例一 爬取搜狗首页的页面源码数据

##### - 基本操作

```python
# 爬取搜狗首页的页面源码数据
import requests						# 导入模块
url = "https://www.sogou.com/"      # 指定URL地址
response = requests.get(url = url)  # 发起请求
page_text =  response.text 			# 获取字符串形式的响应数据
print(page_text)

# 持久化写入到文件中
with open("./sogou.html", mode="w", encoding="utf-8") as f:
    f.write(page_text)

```

##### - 进阶操作

```python
# 实现一个简易的网页采集器
#	- 可以爬取到任意关键字对应的页面源码数据

错误代码一：
    url = 'https://www.sogou.com/web?query=jay'
    response = requests.get(url=url)
    page_text = response.text
    with open('./jay.html','w',encoding='utf-8') as fp:
        fp.write(page_text)
发现的问题：
    - 乱码问题
    - 数据量不对
    - 反爬策略 UA检测机制被触发

问题解决：
	- 乱码问题解决
    	直接返回响应数据的原始编码
        url = 'https://www.sogou.com/web?query=jay'
        response = requests.get(url=url)
        response.encoding = "utf-8"   # 指定编码集
        page_text = response.text
        with open("./jay.html", mode="w", encoding="utf-8") as f:
            f.write(page_text)
            
	- 反爬策略： UA检测破解
		url = 'https://www.sogou.com/web?query=jay'
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        # UA伪装
        response = requests.get(url=url, headers=headers)
        response .encoding = "utf-8"
        page_text = response.text
        with open("./jay.html", mode = "w", encoding = "utf-8") as f:
            f.write(page_text)
            
参数动态化：
	可以动态的给请求指定请求参数：
    key = input("请输入要搜素的内容：")
    #将请求参数封装成键值对
    params = {
        'query':key
    }
    url = 'https://www.sogou.com/web'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    #参数动态化
    response = requests.get(url = url, headers = headers, params = params)

    # response.encoding#返回响应数据原始的编码格式
    response.encoding = 'utf-8'
    page_text = response.text
    fileName = key+'.html'
    with open(fileName,'w',encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName,'爬取成功！！！')
```



#### 案例二  爬取豆瓣中更多电影详情数据

```pytohn
爬取豆瓣中更多电影详情数据：
	当滚轮向下滑动的时候，会加载出更多的电影数据，说明当滚轮滑动到底部时，会发起一个ajax请求，该次请求会加载出更多的数据。
```

##### 数据动态加载

```python
爬取动态加载的数据
	所谓动态加载的数据是指不是通过浏览器地址栏的url请求到的数据。
    
如何检测我们爬取的数据是否为动态加载的数据？
    基于抓包工具做局部搜索（在抓包工具中找到地址栏url对应的数据包，在其response这个选项卡下进行搜索爬取数据的关键字）
    
如何爬取动态加载的数据？
    基于抓包工具做全局搜索，可以帮我们定位到动态加载的数据到底是存在于哪一个数据包中，定位到之后，就可以对该数据包的url进行请求发送捕获数据。
        
动态加载数据的生成方式
	- ajax
    - js
    
日后对一个陌生的网站进行数据爬取，在编码之前必须要做的一件事情是什么？
	检测你要爬取的数据是否为动态加载的数据
		- 如果不是动态加载数据就可以直接对地址栏的url发起请求爬取数据
		- 如果是动态加载数据就需要基于抓包工具进行全局搜索爬取数据

        
常用的抓包工具(主要是应用在移动端数据爬取)比如fiddler,wrieshape等专业工具
    作用:可以拦截请求和相应
        抓包工具就是一个代理服务器
        代理服务器就是进行请求和相应的转发
```

```python
分析：发现滚轮下滑到底部回弹，并且页面刷新除了更多的电影数据
  - 回弹:就是一个ajax请求，页面刷新出来的数据就是ajax请求到的数据

url = "https://movie.douban.com/j/chart/top_list"

params = {
    "type": "5",
    "interval_id": "100:90",
    "action":" ",
    "start": "0",
    "limit": "500",
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}

data_list = requests.get(url = url, headers = headers, params =params).json()
with open("./豆瓣电影.txt", mode = "a+", encoding = "utf-8") as f:
    for dic in data_list:
        title = dic['title']
        score = dic['score']
        release_date = dic['release_date']
        res = "电影名：{}, 上市时间{}, 评分：{}".format(title,score,release_date)  + "\n"
        f.write(res)
        
```



#### 案例三 爬取肯德基餐厅的位置信息

```python
需求：
	http://www.kfc.com.cn/kfccda/storelist/index.aspx
	将北京所有肯德基餐厅的位置信息进行爬取

url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
city = input('请输入要查询的城市名:')
for page in range(5):
    data = {
        'cname': '',
        'pid': '',
        'keyword': city,
        'pageIndex': str(page),
        'pageSize': '10',
    }
    #参数动态化使用的是data参数
    data_dict = requests.post(url=url,headers=headers,data=data).json()
    print(data_dict)
```



#### 案例五：爬取药监总局企业信息

```python
- 需求：
    - url：http://125.35.6.84:81/xk/
    - 将所有企业的详情信息进行爬取保存
- 分析：
    - 尝试着将某一家企业的详情数据爬取到，然后再把此操作作用到其他家企业爬取到所有企业的数据。
    - 检测某一家企业详情数据是否为动态加载的数据
        - 基于抓包工具实现局部搜索
            - 结论：为动态加载数据
    - 基于抓包工具进行全局搜索定位动态加载数据的数据包，从数据包中提取url和请求参数
        - url：http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById
        - 请求方式：post
        - 参数：id: d82345168acb46f8a8b1fad2c8b5adce
        - 通过对比不同企业的详情数据包的信息，发现请求的url，请求方式都一样，只有请求参数id的值不一样而已。
```



```python
# 先获取单个企业的信息
url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
data = {
    'id':'d82345168acb46f8a8b1fad2c8b5adce'
}
detail_json = requests.post(url=url,headers=headers,data=data).json()
per_name = detail_json['businessPerson']  # 企业法人
addr = detail_json['epsAddress']          # 地址
print(per_name,addr)


#尝试着将所有企业的id获取，将其作用到post请求的参数中即可
#思考：id应该是和企业名称关联在一起的，只要找到企业名称就有可能找到企业id，发现企业名称是动态加载的
post_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
for page in range(6):
    data = {
        'on': 'true',
        'page': str(page),
        'pageSize': '15',
        'productName': '',
        'conditionType': '1',
        'applyname': '',
        'applysn':'',
    }
    json_data = requests.post(url=post_url,headers=headers,data=data).json()
    for dic in json_data['list']:
        company_id = dic['ID']
        print(company_id)
        
url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
data = {
    'id':'d82345168acb46f8a8b1fad2c8b5adce'
}
detail_json = requests.post(url=url,headers=headers,data=data).json()
per_name = detail_json['businessPerson']
addr = detail_json['epsAddress']
print(per_name,addr)
```

完整代码

```python
post_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
fp = open('./company_data.txt','a+',encoding='utf-8')
for page in range(6):
    data = {
        'on': 'true',
        'page': str(page),
        'pageSize': '15',
        'productName': '',
        'conditionType': '1',
        'applyname': '',
        'applysn':'',
    }
    json_data = requests.post(url=post_url,headers=headers,data=data).json()
    for dic in json_data['list']:
        company_id = dic['ID']

        url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
        data = {
            'id':company_id
        }
        detail_json = requests.post(url=url,headers=headers,data=data).json()
        per_name = detail_json['businessPerson']
        addr = detail_json['epsAddress']
        print(per_name,addr)
        fp.write(per_name+':'+addr+'\n')
fp.close()
```



#### 案例四：爬取荣耀手机门店信息

```python
url = 'https://openapi.vmall.com/mcp/offlineshop/getShopById?portal=2&version=10&country=CN&shopId=107527&lang=zh-CN'
index_url = 'https://openapi.vmall.com/mcp/offlineshop/getShopList'

data = {"portal":2,"lang":"zh-CN","country":"CN","brand":1,"province":"北京","city":"北京","pageNo":1,"pageSize":20}
data_lst = requests.post(url=index_url, json=data, headers=headers).json()['shopInfos']
for i in data_lst:
    data_msg = {
        'portal': '2',
        'version': '10',
        'country': 'CN',
        'shopId': i['id'],
        'lang': 'zh-CN',
    }
    print(requests.get(url=url, headers=headers, data=data_msg).json()['shopInfo'])
```







#### 案例五：SLC的小店商品信息爬取

```Python
url = 'http://res.91kami.com/Index/Index?q=&p=1&size=20&showInStore=false'
data = {
    'q': '',
    'p': '1',
    'size': '20',
    'showInStore': 'false',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
requests.post(data=data,url=url, headers=headers).json()


返回结果为
	{'IsSuccess': False, 'Error_Code': -1, 'Error_Msg': '拒绝访问', 'AlertMsg': '拒绝访问'}
```

上诉情况虽然加了UA标识，但结果却出现拒绝访问的情况，可能是伪装的不够彻底

	- 通过观察响应头发现该请求中携带Referer，所以加上Referer再次进行测试

```python
url = 'http://res.91kami.com/Index/Index?q=&p=1&size=20&showInStore=false'
data = {
    'q': '',
    'p': '1',
    'size': '20',
    'showInStore': 'false',
} 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer':'http://shop.slc0929.top/'
    }
requests.post(data=data,url=url, headers=headers).json()

```

加入Referer之后发现，请求能够正常访问，因此在出现上诉的错误时，可以加上Referer再次进行测试



#### 爬取图片数据

```python
urllib
requests
	urllib和requests的功能作用都几乎是一致。urllib是一个比较古老的网络请求模块，当requests问世后，就快速的替代了urllib。

#爬取图片方式1
url = 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=4250058738,780121024&fm=11&gp=0.jpg'
#content返回二进制类型的响应数据
img_data = requests.get(url=url,headers=headers).content
with open('123.png','wb') as fp:
    fp.write(img_data)
    

#爬取图片方式2
from urllib import request
url = 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=4250058738,780121024&fm=11&gp=0.jpg'
request.urlretrieve(url=url,filename='./456.png')


上述两者图片爬取方式的区别：
方式1是可以进行UA伪装
方式2无法进行UA伪装
```









