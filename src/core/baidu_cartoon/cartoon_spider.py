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

    @staticmethod
    def run_spider():
        category = CategorySpider()
        category.get_category()
        categoryNames = category.get_category_form_jsonFile()
        print(categoryNames)

        #cartoonPart = CartoonPartSpider(self.__categoryName)
        #cartoonPart.GetComic()


CartoonSpider.run_spider()
