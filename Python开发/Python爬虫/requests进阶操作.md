#### 图片数据爬取

##### 方式一：requests

```Python

import requests
headers = {
    'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

url = 'https://pic.qiushibaike.com/system/pictures/12329/123293159/medium/2UOCOGU7XI5AOK9C.jpg'
response = requests.get(url=url,headers=headers)
#图片，视频，音频都是以二进制数据存在（bytes）
img_data = response.content #返回的是bytes类型的响应数据
with open('./123.png','wb') as fp:
    fp.write(img_data)

```

##### 方式二：urllib

```Python
import urllib #urllib就是一个低级requests
url = 'https://pic.qiushibaike.com/system/pictures/12329/123293159/medium/2UOCOGU7XI5AOK9C.jpg'
urllib.request.urlretrieve(url=url,filename='./456.jpg')
```

两种方法的区别主要在于方法一可以实现UA伪装，方法二不可



#### 案例： 爬取糗事百科中的图片信息

```Python
需求：批量爬取糗事百科中的所有的图片数据
数据解析：可以将页面中指定的局部数据进行提取
三种数据解析方式：
    bs4
    xpath
    pyquery
    
    
浏览器开发者工具中的Elemente和netword选项卡的区别：
    如果浏览器地址栏对应页面中没有动态加载的数据，则这两者显示的页面源码无区别
    如果存在动态加载数据，则Element中显示的页面源码数据表示所有请求加载数据完毕后对应的总数据，而network中仅仅显示地址栏url这一个请求对应的数据。
```

```python
import re,os	#通过正则提取出每一张图片的图片地址

dirName = './libs'		# 图片存放的目录，没有自动创建
if not os.path.exists(dirName):
    os.mkdir(dirName)
    
url = 'https://www.qiushibaike.com/imgrank/'
page_text = requests.get(url=url,headers=headers).text
ex = '<div class="thumb">.*?<img src="(.*?)" alt=.*?</div>'
#一定要注意回车问题:re.S可以让正则表达式忽略回车
img_src_list = re.findall(ex,page_text,re.S)
for src in img_src_list:
    src = 'https:'+src
    img_name = src.split('/')[-1]
    img_path = dirName+'/'+img_name
    
    img_data = requests.get(url=src,headers=headers).content
    with open(img_path,'wb') as fp:
        fp.write(img_data)
    print(img_name,'爬取成功！！！')
```

通过分析不同页码的链接发现，不同页码的链接不同之处仅在于链接的页码不同：

- https://www.qiushibaike.com/imgrank/page/%d/
    - 可以作为一个通用的url模板。可以通过模板动态生成每一个页码的链接



```Python
#将所有页码的图片数据进行爬取
dirName = './libs'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    
url_model = 'https://www.qiushibaike.com/imgrank/page/%d/'#不可变
for page in range(1,14):
    print('正在爬取第%d页的图片数据......'%page)
    new_url = format(url_model%page)
    page_text = requests.get(url=new_url,headers=headers).text
    ex = '<div class="thumb">.*?<img src="(.*?)" alt=.*?</div>'
    #一定要注意回车问题:re.S可以让正则表达式忽略回车
    img_src_list = re.findall(ex,page_text,re.S)
    for src in img_src_list:
        src = 'https:'+src
        img_name = src.split('/')[-1]
        img_path = dirName+'/'+img_name

        img_data = requests.get(url=src,headers=headers).content
        with open(img_path,'wb') as fp:
            fp.write(img_data)
        print(img_name,'爬取成功！！！')
```



#### 案例：爬取站长素材的高清图片

```
任务：
	爬取站长素材-》高清图片，进行爬取
	
URL： 
	https://sc.chinaz.com/tupian/meishi.html
```

```Python
import re
import os

if not os.path.exists('img_pck'):
    os.mkdir('img_pck')
url = 'https://sc.chinaz.com/tupian/meishi.html'
response_data = requests.get(url, headers=headers).text
re_gz = '<div class="box picblock.*?<img src2="(.*?)" alt=".*?</div>'
img_lst = re.findall(re_gz, response_data, re.S)
for url in img_lst:
    new_url = 'https:' + url
    img_info = requests.get(new_url, headers=headers).content
    file_name = new_url.rsplit('/',1)[-1]
    with open('./img_pck/'+file_name, 'wb') as fp:
        fp.write(img_info)
    print(file_name, '下载完成')
```



#### 反爬机制： 图片懒加载

```
图片懒加载，
	图片的img标签中应用了伪属性，只有当触发指定的事件后，伪属性才能变成真正的属性名称
	
什么是图片懒加载：	
	是一种反爬机制,图片懒加载是一种网页优化技术。图片作为一种网络资源，在被请求时也与普通静态资源一样，将占用网络资源，而一次性将整个页面的所有图片加载完，将大大增加页面的首屏加载时间。为了解决这种问题，通过前后端配合，使图片仅在浏览器当前视窗内出现时才加载该图片，达到减少首屏图片请求数的技术就被称为“图片懒加载”
	
如何实现图片懒加载
	在网页源码中，在img标签中首先会使用一个“伪属性”（通常使用src2，original…）去存放真正的图片链接而并非是直接存放在src属性中。当图片出现到页面的可视化区域中，会动态将伪属性替换成src属性，完成图片的加载。

```

#### 案例：爬取站长之家的图片素材

```python
# 图片懒加载案例

import scrapy
import requests
headers={
'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

class ImgzzSpider(scrapy.Spider):
    name = 'imgzz'

    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        src = response.xpath('//*[@id="container"]/div/div[1]/a/img/@src').extract()
	    print(src) # 打印结果为空,这里的图片属性就应用的图片懒加载技术,其实图片的真正的src不是图片真正的属性
        for url in src:
            name = url.split('/')[-1]
            img = requests.get(url=url,headers=headers).content
            with open(name,'wb') as f:
                f.write(img)
     
# 修正后

import scrapy
import requests
headers={
'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

class ImgzzSpider(scrapy.Spider):
    name = 'imgzz'

    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        src = response.xpath('//*[@id="container"]/div/div[1]/a/img/@src2').extract() #改为图片的真正属性
	    print(src) 
        for url in src:
            name = url.split('/')[-1]
            img = requests.get(url=url,headers=headers).content
            with open(name,'wb') as f:
                f.write(img)
```





#### 反爬机制 robots协议

```Python
robots.txt协议
    指定了网站中可爬和不可爬的目录
    没有采用强硬的相关机制阻止爬虫的爬取
  
参考链接
	https://developers.google.com/search/docs/advanced/robots/robots_txt



```



#### cookie反爬

```Python
在爬虫中处理cookie的方式：
	手动处理
		从抓包工具中将cookie封装到headers字典中
		局限性：如果cookie过了有效时长，则该种方式会失效
	自动处理
        使用session机制。
        1.可以获取一个session对象
        2.可以基于该对象进行请求的发送
        在请求发送的过程中，如果产生了cookie，则cookie会被存储到该对象中。
        如果cookie被存储到了session对象中，则再次使用session对象发请求，则该次请求就是携带者cookie进行的请求发送
        注意：Session对象在使用的时候，至少需要被调用两次。

```

##### 案例： 爬取雪球网中的资讯数据

```Python
需求：
	爬取雪球网中的咨询数据
    
url：
	https://xueqiu.com/
        
        
url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=72813&size=15'
requests.get(url,headers=headers).json()
#问题：没有获取数据，原因一定是没有严格模拟浏览器上网的流程
#返回信息
    {'error_description': '遇到错误，请刷新页面或者重新登录帐号后再试',
     'error_uri': '/statuses/hot/listV2.json',
     'error_data': None,
     'error_code': '400016'}
```

```Python
sess = requests.Session() #创建了一个sessio对象
first_url = 'https://xueqiu.com/'
#该次请求会产生cookie，且cookie存储到了session对象中
sess.get(url=first_url,headers=headers)

url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=72813&size=15'
#该次请求就是携带cookie进行的请求发送
sess.get(url,headers=headers).json()
```



#### 代理反爬

```Python
什么是代理：
	就是代理服务器
    
代理服务器的作用：
	可以进行请求和响应的转发/拦截
    
在爬虫中为何需要使用代理？
	如果我们使用爬虫对一个网站在段时间内发起一个高频的请求，该网站会检测出这个异常的现象，且会将异常的请求ip获取，将ip加入到黑名单，然后该ip在近期就无法再次对该网站进行网络访问。
	如果本机ip被对方服务器加入到了黑名单，则我们就可以使用代理服务器进行请求转发，最终对方服务器获取的请求ip就是代理服务器的不在我们自己本机的。
    
代理的匿名度：
    透明：对方服务器知道你使用了代理，也知道你的真实ip
    匿名：对方服务器知道你使用了代理，但是不知道你的真是ip
    高匿：不知道使用了代理，也不知道你的真实ip
    
代理的类型：
    http：只能转发http协议的请求
    https：只能转发https协议的请求
```

```Python
from lxml import etree

#没有使用代理的情况
url = 'https://www.sogou.com/web?query=ip'
page_text = requests.get(url=url,headers=headers).text
tree = etree.HTML(page_text)
tree.xpath('//*[@id="ipsearchresult"]//text()')


# 返回信息
['本机IP：',
 '221.218.208.96\xa0\xa0\xa0\n\n                未知来源\n        ',
 '\n    ']
```

```Python

#使用代理的情况
url = 'https://www.sogou.com/web?query=ip'
page_text = requests.get(url=url,headers=headers,proxies={'https':'114.239.119.157:42559'}).text
tree = etree.HTML(page_text)
tree.xpath('//*[@id="ipsearchresult"]//text()')

# 返回信息
```

推荐代理网站：

​	https://www.zhiliandaili.cn/



##### 案例：代理池构建

```Python
需求：
	对一个网站发起高频请求，然后让其将本机ip加入黑名单，构建代理池处理

如何处理动态变化的请求参数
    将动态变化的请求参数隐藏在前台页面中
    基于抓包工具进行全局搜索

```

```Python
import random

#提取代理精灵代理服务器ip+port的方法
all_proxy = [] #代理池
url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=51&time=1&pro=&city=&port=1&format=html&ss=5&css=&dt=1&specialTxt=3&specialJson=&usertype=2'
page_text = requests.get(url,headers=headers).text
tree = etree.HTML(page_text)
data_list = tree.xpath('//body//text()')
for data in data_list:
    dic = {}
    dic['https'] = data
    all_proxy.append(dic)
    

url_model = 'http://www.521609.com/daxuemeinv/list8%d.html'
all_data = []
for page in range(1,23):
    url = format(url_model%page)
    page_text = requests.get(url=url,headers=headers,proxies=random.choice(all_proxy)).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="content"]/div[2]/div[2]/ul/li')
    for li in li_list:
        detail_url = 'http://www.521609.com'+li.xpath('./a[1]/@href')[0]
        page_text_detail = requests.get(detail_url,headers=headers).text
        all_data.append(page_text_detail)
print(len(all_data))
```

