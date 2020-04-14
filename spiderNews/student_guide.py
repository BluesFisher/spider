#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)
reload(sys)
sys.setdefaultencoding('utf8')

import json
import copy
import time
from common.json_func import JsonFunc
from common_func import CommonFunc

list_items = {}


def get_info():
    global list_items

    list_items, detail_info = CommonFunc().get_student_guide('', list_items)
    num = 0
    for item in copy.deepcopy(list_items).keys():
        list_items[item] = CommonFunc().get_news_detail(
            list_items[item]['url'], list_items[item])
        num += 1

    print json.dumps(list_items, encoding='UTF-8',
                     ensure_ascii=False), len(list_items.keys())


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    get_info()
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    JsonFunc().save_json(list_items, path + '/news/student_guid_' + date)

    # url = 'http://www.gaokao.com/e/20200312/5e6a165d1060f.shtml' # img
    # url = 'http://www.gaokao.com/e/20200326/5e7c0b3a2aeca.shtml' # normal
    # url = 'http://www.gaokao.com/e/20200319/5e735b65e2da7.shtml'  # table
    # detail_info = CommonFunc().get_news_detail(url, {})
    # print json.dumps(detail_info, encoding='UTF-8', ensure_ascii=False)
