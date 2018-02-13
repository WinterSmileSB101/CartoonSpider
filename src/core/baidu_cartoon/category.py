import urllib
import re
import os
import urllib.request as req
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
from pprint import pprint
from utils import BaiDuCartoonUtils
import os.path

url = "http://cartoon.baidu.com/category"

filePath = r"D:/Alvin/PersonalProjects/Python/Spider/CartoonSpider/file/categories/"

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# 设置代理 IP，http 不行，使用 https
proxy = req.ProxyHandler({'https': 's1firewall:8080'})
auth = req.HTTPBasicAuthHandler()
# 构造 opener
opener = req.build_opener(proxy, auth, req.HTTPHandler)
# 添加 header
opener.addheaders = [('User-Agent', user_agent)]
# 安装 opener
req.install_opener(opener)
# 打开链接
conn = req.urlopen(url)
# 以 utf-8 编码获取网页内容
content = conn.read().decode('utf-8')
# 输出
print(content)

# 生成 soup 对象，准备解析 html
soup = BeautifulSoup(content,'lxml')

print(soup.find_all(re.compile('^{"/api/category"+}}')))

scripts = soup.find_all("script")
for script in scripts:
    if '/api/category' in script.get_text():
        # 获取内容
        print(script.get_text().split('=')[1].strip())
        # 转化成 Json
        categoryJson = json.loads(script.get_text().split('=')[1].strip())
        # pprint(categoryJson['/api/category'])
        # 判断路径是否存在
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        # 必须加上编码方式，否则中文会乱码
        with open(filePath + 'data.json', 'w', encoding='utf-8') as f:
            json.dump(categoryJson, f, ensure_ascii=False) # 这里必须要禁用系统的 ascii 编码方式
            print("写入完成")

        categoryList = categoryJson['/api/category']['data']['list']
        for category in categoryList:
            # 判断路径是否存在
            if not os.path.exists(filePath + category['name'] + '/'):
                os.makedirs(filePath + category['name'] + '/')
            # 写入图片文件
            req.urlretrieve(category['img'], filePath + category['name'] + '/' + category['name']+'.png')