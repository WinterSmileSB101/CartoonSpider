import urllib
import re
import os
import urllib.request as req
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
from utils import BaiDuCartoonUtils
from cartoon_part_spider import CartoonPartSpider
from category_spider import CategorySpider

class CartoonSpider(object):


    def __init__(self, categoryName):
        self.__categoryName = categoryName
        self.__filePath = r"D:/Alvin/PersonalProjects/Python/Spider/CartoonSpider/file/categories/"+categoryName+'/'
        self.__baseUrl = 'http://cartoon.baidu.com/api/query/'
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

    def GetCartoonJson(self):
        hasMore = True
        index = 1
        while hasMore:
            link = self.__baseUrl + self.__categoryName+'/'+str(index)
            # 转换中文 url 编码
            link = urllib.request.quote(link)
            print(link)
            # 把多余的转换 : ==> %3A ，还原
            link = link.replace('%3A', ':')
            # 打开链接
            conn = req.urlopen(link)
            # 以 utf-8 编码获取网页内容
            content = conn.read().decode('utf-8')
            print(content)
            jsonUtils = BaiDuCartoonUtils(self.__filePath)
            jsonUtils.write_json_to_jsonFile(content,self.__filePath,'data'+str(index)+'.json')

            jsonStr = json.loads(content)
            if jsonStr['data']['hasMore']!=1:
                hasMore=False
            index = index+1
            # jsonUtils.write_cartoon_to_json('/api/query/'+self.__categoryName, content)

    def runSpider(self):
        cartoonCategory = CategorySpider()
        cartoonCategory.get_category()
        cartoonCategory.get_category_form_jsonFile()

        #self.GetCartoonJson()
        #cartoonPart = CartoonPartSpider(self.__categoryName)
        #cartoonPart.GetComic()


cartoon = CartoonSpider('都市')
cartoon.runSpider()
