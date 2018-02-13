import json
from bs4 import BeautifulSoup
import bs4
import os


class BaiDuCartoonUtils(object):

    def __init__(self, file_path):
        self.__filePath = file_path

    def write_cartoon_to_json(self, main_name, bs_node,fields,id):
        if not isinstance(main_name, str):
            raise TypeError('bad operand type')
        if not isinstance(bs_node, str):
            raise TypeError('bad operand type of bs_node')
        soup = BeautifulSoup(bs_node, 'lxml')
        scripts = soup.find_all("script")
        print(scripts)
        for script in scripts:
            if main_name in script.get_text():
                print(script.get_text())
                # 获取内容
                print(script.get_text().split(' = ')[1].strip())
                # 转化成 Json
                categoryJson = json.loads(script.get_text().split(' = ')[1].strip())
                # pprint(categoryJson['/api/category'])
                # 判断路径是否存在
                if not os.path.exists(self.__filePath):
                    os.makedirs(self.__filePath)
                # 必须加上编码方式，否则中文会乱码
                with open(self.__filePath + id+'.json', 'w', encoding='utf-8') as f:
                    json.dump(categoryJson[fields], f, ensure_ascii=False)  # 这里必须要禁用系统的 ascii 编码方式
                    print("写入完成")

    def write_json_to_jsonFile(self, content, filePath,fileName):
        if not isinstance(content, str):
            raise TypeError('bad operand type')
        if not isinstance(filePath, str):
            raise TypeError('bad operand type of bs_node')
        if not isinstance(fileName, str):
            raise TypeError('bad operand type of bs_node')

        # 转化成 Json
        categoryJson = json.loads(content)
        # pprint(categoryJson['/api/category'])
        # 判断路径是否存在
        if not os.path.exists(self.__filePath):
            os.makedirs(self.__filePath)
        # 必须加上编码方式，否则中文会乱码
        with open(self.__filePath + fileName, 'w', encoding='utf-8') as f:
            json.dump(categoryJson, f, ensure_ascii=False)  # 这里必须要禁用系统的 ascii 编码方式
            print("写入完成")

    # 获取漫画的信息
    def get_cartoon_from_json(self, filePath,categoryName):
        if not isinstance(filePath, str):
            raise TypeError('bad operand type')
        if not isinstance(categoryName, str):
            raise TypeError('bad operand type of bs_node')
        if os.path.exists(self.__filePath):
            with open(self.__filePath + 'data.json', 'r', encoding='utf-8') as f:
                # reading data from json
                resp = json.load(f)
                return resp['/api/query/'+categoryName]['data']['list']
        return None

    # 获取漫画的信息
    def get_jsonStr_from_jsonFile(self, filePath):
        if not isinstance(filePath, str):
            raise TypeError('bad operand type')
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                # reading data from json
                resp = json.load(f)
                return resp
        return None

