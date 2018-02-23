from src.core.baidu_cartoon.cartoon_spider import CartoonSpider


class Programm(object):

    def __init__(self):
        self.__start = 'Baidu'

    @staticmethod
    def run():
        CartoonSpider.run_spider()

Programm.run()