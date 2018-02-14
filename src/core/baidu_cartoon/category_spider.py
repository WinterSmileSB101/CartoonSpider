import urllib
import re
import os
import urllib.request as req
from urllib.request import urlretrieve

from anaconda_project.internal import http_client
from bs4 import BeautifulSoup
import json
from pprint import pprint
from utils import BaiDuCartoonUtils
import os.path


class CategorySpider(object):

    def __init__(self):
        self.__fileName = 'data.json'
        self.__baseUrl='http://cartoon.baidu.com/api/category'
        self.__filePath = r"D:/Alvin/PersonalProjects/Python/Spider/CartoonSpider/file/categories/"
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
        for category in categories:
            hasMore = True
            index = 1
            while hasMore:
                try:
                    link = self.__baseUrl + '/' + category['name']+'/'+str(index)
                    # 转换中文 url 编码
                    link = urllib.request.quote(link)
                    print(link)
                    # 把多余的转换 : ==> %3A ，还原
                    link = link.replace('%3A', ':')
                    # 打开链接
                    conn = req.urlopen(link)
                    # 以 utf-8 编码获取网页内容
                    content = conn.read().decode('utf-8')

                except http_client.IncompleteRead as e:
                    # 处理 chunked 读取错误，由于这里都是 json 所以就不再作 gzip 验证
                    content = e.partial
                    content = content.decode('utf-8')
                    if len(content) == 0:
                        content = '{}'

                print(content)
                jsonUtils = BaiDuCartoonUtils(self.__filePath)
                jsonUtils.write_json_to_jsonFile(content, self.__filePath + category['name'] + '/list/',
                                                 'data' + str(index) + '.json')

                jsonStr = json.loads(content)
                if jsonStr['data']['hasMore'] != 1:
                    hasMore = False
                index = index + 1
                # jsonUtils.write_cartoon_to_json('/api/query/'+self.__categoryName, content)

    def get_category_form_jsonFile(self):
        # 获取所有文件夹名称
        dirNames = [name for name in os.listdir(self.__filePath)
                    if os.path.isdir(os.path.join(self.__filePath, name))]
        print(dirNames)

    def run(self):
        self.get_category()

categorySpider = CategorySpider()
categorySpider.run()