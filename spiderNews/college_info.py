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
import datetime
from common.json_func import JsonFunc
from common_func import CommonFunc

list_items = []


def get_info():
    global list_items

    list_items, detail_info = CommonFunc().get_college_info('', list_items)
    now_date = datetime.datetime.strptime(str(datetime.date.today()),
                                          '%Y-%m-%d')
    num = 0
    for item in copy.deepcopy(list_items):
        news_date = datetime.datetime.strptime(item['date'],
                                               '%Y-%m-%d %H:%M:%S')
        if news_date.__lt__(now_date):
            print item['date']
            list_items = list_items[0:num]
            break
        list_items[num] = CommonFunc().get_college_info_detail(
            item['url'], item)
        num += 1

    print json.dumps(list_items, encoding='UTF-8', ensure_ascii=False)


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    get_info()
    date = time.strftime('%m%d', time.localtime(time.time()))
    JsonFunc().save_json(list_items, path + '/news/college_info_' + date)

    # url = 'http://www.gaokao.com/e/20200312/5e6a165d1060f.shtml' # img
    # url = 'http://www.gaokao.com/e/20200326/5e7c0b3a2aeca.shtml' # normal
    # url = 'http://www.gaokao.com/e/20200319/5e735b65e2da7.shtml'  # table
    # detail_info = CommonFunc().get_college_info_detail(url, {})
    # print json.dumps(detail_info, encoding='UTF-8', ensure_ascii=False)
