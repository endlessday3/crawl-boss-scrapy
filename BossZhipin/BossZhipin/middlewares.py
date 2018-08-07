# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import threading

import requests
from fake_useragent import UserAgent

from BossZhipin.settings import PROXIES


class RandomUserAgent:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        user_agent = self.ua.random
        request.headers["User-Agent"] = user_agent


class RandomProxy:
    def __init__(self):
        # json_array = requests.get(
        #     "http://dec.ip3366.net/api/?key=20180613161424534&getnum=60&anonymoustype=4&filter=1&area=1&order=2&formats=2&proxytype=0").json()
        # self.proxy_list = json_array
        #
        # # 创建一个定时器，每过30s更新一下代理ip池
        # self.timer = threading.Timer(60 * 5, self.timer_task)
        # self.timer.start()
        self.proxy_list = PROXIES

    def process_request(self, request, spider):
        # proxy_dict = dict(random.choice(self.proxy_list))
        # ip = str(proxy_dict["Ip"])
        # port = str(proxy_dict["Port"])
        # print(ip + ":" + port)
        #
        # request.meta['proxy'] = "http://" + ip + ":" + port
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = "http://" + proxy
        print("===", request.meta, "===", request.headers)

    def process_response(self, request, response, spider):
        """
            对返回的response处理
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # proxy_dict = random.choice(self.proxy_list)
            # ip = str(proxy_dict["Ip"])
            # port = str(proxy_dict["Port"])
            # print("get a new response ip:" + ip + " ：" + port)
            # # 对当前request加上代理
            # request.meta['proxy'] = "http://" + ip + ":" + port

            proxy = random.choice(self.proxy_list)
            print("get a new request ip:" + proxy)
            request.meta['proxy'] = "http://" + proxy
            return request
        return response

    # def timer_task(self):
    #     json_array = requests.get(
    #         "http://dec.ip3366.net/api/?key=20180613161424534&getnum=50&anonymoustype=4&filter=1&area=1&order=2&formats=2&proxytype=0")\
    #         .json()
    #     self.proxy_list = json_array
