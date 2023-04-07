#!/usr/bin/python
# -*- coding: UTF-8 -*-

from fake_useragent import UserAgent
from common import COMMON_PATH
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
        location = COMMON_PATH[mod] + 'fake_useragent.json'
        ua = UserAgent(path=location)
        return ua.random

    def set_request(self, url):
        print 'Request', url
        if not url:
            return {'text': ''}

        # proxy = { 'http': 'http://' + proxy_list[random.randint(0,len(proxy_list) - 1)] }
        # res = requests.get(url, headers=headers, proxies=proxy)
        headers = {'user-agent': self.get_header(), 'uuid': '18759dc5510c8-1e738c3919cf03-0-0-18759dc5510c8','token': 'AgGkI8Q86H7DI0CyTgPWdVXis31z0wi3U75QJjvtGRDbD0lwpjIscJ-RuHPdcbph2NXfzGVcGq59bwAAAACdFwAATmpiLl9EuTuVm-lr4KwOGMbiAMRmBkMSbpeW6OPxeLfkbYscdnSMyFQN19wRivkc', 'openId': 'oJVP50FqTESXFWoA0CrQqT4_5zgA', 'clientversion': '2.30.4', 'M-TRACEID': '3019535102683527080', 'openIdCipher': 'AwQAAABJAgAAAAEAAAAyAAAAPLgC95WH3MyqngAoyM/hf1hEoKrGdo0pJ5DI44e1wGF9AT3PH7Wes03actC2n/GVnwfURonD78PewMUppAAAADjRujQWnsTxZOc5jzkVvUKUvNU14lydaS+iNa/y3GwJK8b1v4frcTJzKkbxqGbvaQtatowA9PMPpw==', 'Referer': 'https://servicewechat.com/wxde8ac0a21135c07d/1130/page-frame.html'}
        res = requests.get(url, headers=headers)
        return res
