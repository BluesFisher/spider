#!/usr/bin/python
# -*- coding: UTF-8 -*-

from fake_useragent import UserAgent
from common import PROFESSION_UA_PATH
import requests
import logging

logging.basicConfig()

proxy_list = [
    '221.122.91.66:80'
    # '59.62.7.186:9000',
    # '27.214.50.175:9000',
    # '223.241.117.120:8010',
    # '27.220.121.211:9000',
    # '27.220.120.142:9000'
]


class Request(object):
    def __init__(self):
        self.url = {
            'pro_list_url': 'http://college.gaokao.com/spelist/',  # 专业列表
            'pro_url': 'http://college.gaokao.com/speciality/',  # 专业介绍
            'college_info': 'http://www.gaokao.com/guangdong/gdxw/',  # 高考资讯
            'student_guide': 'http://www.gaokao.com/guangdong/zsjz/',  # 招生简章
            'college_dynamic': 'http://www.gaokao.com/guangdong/yx/',  # 院校动态
            'college_detail': 'http://college.gaokao.com/schlist/a14/'  # 院校详情
        }
        pass

    def get_url(self, url, mod='pro_url'):
        return url if 'http' in url else (self.url[mod] + url)

    def get_header(self, mod='default'):
        location = PROFESSION_UA_PATH[mod] + 'fake_useragent.json'
        ua = UserAgent(path=location)
        return ua.random

    def set_request(self, url):
        print 'Request', url
        if not url:
            return {'text': ''}

        # proxy = { 'http': 'http://' + proxy_list[random.randint(0,len(proxy_list) - 1)] }
        # res = requests.get(url, headers=headers, proxies=proxy)
        headers = {'user-agent': self.get_header()}
        res = requests.get(url, headers=headers)
        return res
