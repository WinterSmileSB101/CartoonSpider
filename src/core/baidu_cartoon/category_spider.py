import urllib
import re
import os
import urllib.request as req
from urllib.request import urlretrieve

from anaconda_project.internal import http_client
from bs4 import BeautifulSoup
import json
from pprint import pprint
import os.path

from src.core.baidu_cartoon.utils import BaiDuCartoonUtils


class CategorySpider(object):

    def __init__(self):
        self.__fileName = 'data.json'
        self.__baseUrl='http://cartoon.baidu.com/api/category'
        self.__filePath = r"H:/GIT/Python/Spider/CartoonSpider/file/categories/"
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

    def get_category(self):
        link = self.__baseUrl
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
        jsonUtils.write_json_to_jsonFile(content, self.__filePath+'list/', self.__fileName)

        Categories = json.loads(content)['data']['list']
        self.get_cartoon_json(Categories)

    def get_cartoon_json(self,categories):
        print("getcategoryjson")

        for category in categories:
            hasMore = True
            index = 1
            while hasMore:
                category_content = ''
                try:
                    # 判断文件是否存在
                    if not os.path.exists(self.__filePath + category['name'] + '/list/data' + str(index) + '.json'):
                        link = self.__baseUrl + '/' + category['name']+'/'+str(index)
                        # 转换中文 url 编码
                        link = urllib.request.quote(link)
                        # 把多余的转换 : ==> %3A ，还原
                        link = link.replace('%3A', ':')
                        print(categories)
                        # 打开链接
                        print(link)
                        conn = req.urlopen(link)
                        # 以 utf-8 编码获取网页内容
                        category_content = conn.read().decode('utf-8')

                except http_client.IncompleteRead as e:
                    # 处理 chunked 读取错误，由于这里都是 json 所以就不再作 gzip 验证
                    category_content = e.partial
                    category_content = category_content.decode('utf-8')
                    if len(category_content) == 0:
                        category_content = '{}'

                print(category_content)
                if len(category_content)>0:
                    jsonUtils = BaiDuCartoonUtils(self.__filePath)
                    jsonUtils.write_json_to_jsonFile(category_content, self.__filePath + category['name'] + '/list/',
                                                     'data' + str(index) + '.json')

                    jsonStr = json.loads(category_content)
                    if jsonStr['data']['hasMore'] != 1:
                        hasMore = False
                    index = index + 1
                else:
                    hasMore = False

                # jsonUtils.write_cartoon_to_json('/api/query/'+self.__categoryName, content)

    def get_category_form_jsonFile(self):
        # 获取所有文件夹名称
        dirNames = [name for name in os.listdir(self.__filePath)
                    if os.path.isdir(os.path.join(self.__filePath, name)) and name!='list']
        return dirNames

    def run(self):
        # self.get_category()
        self.get_category_form_jsonFile()