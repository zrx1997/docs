Selenium自动化框架

- 实现浏览器自动化的相关操作!
- 环境安装:pip install selenium
- 下载浏览器的驱动程序(下载高版本的驱动)
    - http://npm.taobao.org/mirrors/chromedriver/



```Python
# 简单使用

from selenium import webdriver
from time import sleep

#1.实例化一款浏览器对象
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
#2.发起请求
bro.get('https://www.jd.com/')
#3.标签定位
text_input = bro.find_element_by_xpath('//*[@id="key"]')
#4.向指定标签中录入文本
text_input.send_keys('iphone 12')
sleep(1)
btn = bro.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
btn.click()
sleep(1)
#5.js注入，滑动到底部
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)
bro.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[7]').click()
sleep(3)
#关闭浏览器
bro.quit()

```





selenium和爬虫之间的关联

- 可以便捷的捕获到动态加载的数据(可见即可得)
- 可以实现模拟登陆



```Python
#捕获动态加载数据
from lxml import etree

bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.get('http://scxk.nmpa.gov.cn:81/xk/')
sleep(1)
#page_source返回当前打开的页面源码数据(包含动态加载数据)
page_text = bro.page_source
page_text_list = [page_text]#保存前五页的页面源码数据

for i in range(5):
    bro.find_element_by_xpath('//*[@id="pageIto_next"]').click()
    sleep(1)
    page_text_list.append(bro.page_source)

for page_text in page_text_list:
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="gzlist"]/li')
    for li in li_list:
        title = li.xpath('./dl/@title')[0]
        print(title)
bro.quit()
```



- 动作链
    - 封装了很多连续的行为动作

```
from selenium.webdriver import ActionChains
```

- 如果直接定位一个子页面中的标签,会报错
    - 解决:使用switch_to函数处理
        - bro.switch_to.frame('iframe的id')



```
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
sleep(1)
bro.switch_to.frame('iframeResult')
div_tag = bro.find_element_by_xpath('//*[@id="draggable"]')

#1.实例化动作链对象且将动作链关联到当前浏览器
action = ActionChains(bro)
#2.制定行为动作
action.click_and_hold(div_tag) #点击且长按
for i in range(5):
    action.move_by_offset(7,5).perform()#perform表示让动作链立即执行
    sleep(0.5)
sleep(2)
bro.quit()
```

- cookie的处理



```
browser = webdriver.Chrome(executable_path='./chromedriver.exe')
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())

browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})
print(browser.get_cookies())

browser.delete_all_cookies()

print(browser.get_cookies())
```

- 无头浏览器
    - 无可视化界面的浏览器(谷歌)

```
from selenium.webdriver.chrome.options import Options
# 创建一个参数对象，用来控制chrome以无界面模式打开
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


browser = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=chrome_options)
browser.get('https://www.zhihu.com/explore')
print(browser.page_source)
browser.save_screenshot('./zhihu.jpg') #截图
browser.quit()
```

#### 案例： 模拟12306登录

```python
#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()
    
#定义一个识别验证码图片的函数
def getCode_text(imgPath,imgType):
    chaojiying = Chaojiying_Client('227851369', '123456', '	911685')	
    im = open(imgPath, 'rb').read()
    return chaojiying.PostPic(im,imgType)['pic_str']



from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
#pip install PIL (Pillow)
from PIL import Image

# 裁剪验证码， 图片裁剪务必将电脑的缩放比例调成100%

bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.get('https://kyfw.12306.cn/otn/login/init')
sleep(1)
#截屏
bro.save_screenshot('main.png') #截取的是当前完整的页面图片
#获取验证码图片左下角和右上角两点坐标
img_tag = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')
#左下角坐标
location = img_tag.location
#返回验证码图片的尺寸
size = img_tag.size
#指定裁剪的范围
rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
i = Image.open('./main.png')
frame = i.crop(rangle)#根据裁剪的范围进行裁剪
frame.save('code.png')

#验证码识别，返回点击坐标
result = getCode_text('code.png',9004)
print(result) #:x1,y1|x2,y2|x3,y3
#将result转换成[[x1,y1],[x2,y2]]
all_list = []
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
    
for loc in all_list:
    x = loc[0]
    y = loc[1]
    ActionChains(bro).move_to_element_with_offset(img_tag,x,y).click().perform()
    sleep(1)
bro.find_element_by_id('username').send_keys('1234567890')
sleep(1)
bro.find_element_by_id('password').send_keys('0000000000')
sleep(1)
#验证码的处理

bro.find_element_by_id('loginSub').click()
sleep(3)
bro.quit()
```

- phantomJs:一款无头浏览器
- appnium:基于手机app的自动化模块

