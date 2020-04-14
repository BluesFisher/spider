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
import time
from common.json_func import JsonFunc
from common_func import CommonFunc

list_items = {}
START_NUM = 1
END_NUM = 5


def get_info(start_num, end_num):
    global list_items

    for num in range(start_num, end_num + 1):
        url = 'p' + str(num) + '/'
        detail_info = {"p": num}
        list_items, detail_info = CommonFunc().get_college_detail(
            url, list_items)

    print json.dumps(list_items, encoding='UTF-8',
                     ensure_ascii=False), len(list_items.keys())


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    get_info(START_NUM, END_NUM)
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    JsonFunc().save_json(list_items, path + '/college/college_detail_' + date)
