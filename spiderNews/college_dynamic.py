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
from common.sql_obj import SqlObj
from common.utils import Utils

list_items = []


def get_info():
    global list_items

    list_items, detail_info = CommonFunc().get_college_info(
        '', list_items, mod='college_dynamic')
    now_date = datetime.datetime.strptime(str(datetime.date.today()),
                                          '%Y-%m-%d')
    num = 0
    for item in copy.deepcopy(list_items):
        news_date = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
        if news_date.__lt__(now_date):
            print item['date']
            list_items = list_items[0:num]
            break
        list_items[num] = CommonFunc().get_news_detail(item['url'], item)
        num += 1

    print json.dumps(list_items, encoding='UTF-8',
                     ensure_ascii=False), len(list_items)


def save_db(path):
    try:
        with open(path + '.json') as fp:
            data = fp.read()
            sql_obj = SqlObj()
            insert_data = []
            for item in json.loads(data):
                insert_data.append({
                    'url':
                    item['url'].encode('gbk'),
                    'date':
                    item['date'].encode('gbk'),
                    'title':
                    Utils().unicode_convert(item['title']),
                    '`desc`':
                    Utils().unicode_convert(item['desc']),
                    'content':
                    Utils().unicode_convert(
                        json.dumps(item['content'], ensure_ascii=False))
                })

            sql_obj.insert('t_college_dynamic', insert_data, True)
        print 'save_db ok'
    except Exception as error:
        print 'save_db failed: ', error


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_path = path + '/news/college_dynamic_' + date

    get_info()
    JsonFunc().save_json(list_items, file_path)

    save_db(file_path)
