#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)

import time
from common.request import Request
from common.json_func import JsonFunc
from bs4 import BeautifulSoup
from common_func import CommonFunc

reload(sys)
sys.setdefaultencoding('utf8')

START_NUM = 71
END_NUM = 71

list_items = {}
detail_info = {}
name = ''
request = Request()
PATH = PAR_DIR + '/data/profession'


def get_info(start_num, end_num):
    global list_items
    global detail_info

    for num in range(start_num, end_num + 1):
        url = request.get_url('p' + str(num) + '/', mod='pro_list_url')
        itemLink = ''
        try:
            res = request.set_request(url)
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find('div', {'class': 'scores_List'})
            domList = dom.find_all('dl')

            print 'ok: ', url
            for item in domList:
                # 专业链接
                itemLink = item.find_all('a')[0]['href']
                detail_info = {"p": num}
                for subItem in item.find_all('li'):
                    info = subItem.get_text().strip().split('：')
                    detail_info[info[0]] = info[1]
                try:
                    list_items, detail_info = CommonFunc().get_pro_info(
                        itemLink, list_items, detail_info, mod='pro_list_url')
                except IOError:
                    time.sleep(5)
                    pass
        except IOError:
            print 'failed: ', url
        finally:
            JsonFunc().save_json(list_items,
                                 PATH + '/profile/profession_' + str(num))
            list_items = {}
            time.sleep(30)
            pass


if __name__ == '__main__':
    get_info(START_NUM, END_NUM)
    # html = set_request('http://ip.chinaz.com/')
    # html=BeautifulSoup(html.text,"html.parser")
    # html=html.select('.getlist')
    # print(html)
