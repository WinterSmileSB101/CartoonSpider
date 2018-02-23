import urllib
import re
import os
import urllib.request as req
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
import os.path
from src.core.baidu_cartoon.utils import BaiDuCartoonUtils


class CartoonPartSpider(object):

    def __init__(self, categoryName):
        self.__categoryName = categoryName
        self.__filePath = r"H:/GIT/Python/Spider/CartoonSpider/file/categories/" + categoryName+'/list/'
        self.__baseUrl = 'http://cartoon.baidu.com/comic/'
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

    def GetComic(self):
        # 获取所有文件名称
        dirNames = [name for name in os.listdir(self.__filePath)
                    if os.path.isfile(os.path.join(self.__filePath,name))]
        # 遍历路径，漫画的 json 以及图片（图片通过替换 chapter_url 中的 index.html 为 action.php,index 为 章节的编号，遍历 allChapterList ）
        for fileName in dirNames:
            jsonUtils = BaiDuCartoonUtils(self.__filePath)
            comics = jsonUtils.get_jsonStr_from_jsonFile(self.__filePath+fileName)['data']['list']
            for comic in comics:
                link = self.__baseUrl + comic['id']
                print(link)
                conn = req.urlopen(link)

                # 以 utf-8 编码获取网页内容
                content = conn.read().decode('utf-8')
                print(content)
                # write_cartoon_to_json
                #jsonUtils.write_json_to_jsonFile(content, self.__filePath+'/'+comic['title'], 'data.json')
                #('/api/query/'+self.__categoryName, content)
                jsonUtils = BaiDuCartoonUtils(self.__filePath+comic['title']+'/')
                jsonUtils.write_cartoon_to_json('/api/comic/'+comic['id'],content,'/api/comic/'+comic['id'],comic['id'])