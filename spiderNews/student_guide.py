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
from common.sql_obj import SqlObj
from common.utils import Utils

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


def save_db(path):
    try:
        with open(path + '.json') as fp:
            data = json.loads(fp.read())
            sql_obj = SqlObj()
            insert_data = []
            for item in data.keys():
                insert_data.append({
                    'college':
                    item.encode('utf8'),
                    'url':
                    data[item]['url'].encode('gbk'),
                    'content':
                    Utils().unicode_convert(
                        json.dumps(data[item]['content'], ensure_ascii=False))
                })

            sql_obj.insert('t_student_guide', insert_data, True)
        print 'save_db ok'
    except Exception as error:
        print 'save_db failed: ', error


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_path = path + '/news/student_guide_' + date

    get_info()
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    JsonFunc().save_json(list_items, file_path)

    save_db(file_path)

    # url = 'http://www.gaokao.com/e/20200312/5e6a165d1060f.shtml' # img
    # url = 'http://www.gaokao.com/e/20200326/5e7c0b3a2aeca.shtml' # normal
    # url = 'http://www.gaokao.com/e/20200319/5e735b65e2da7.shtml'  # table
    # detail_info = CommonFunc().get_news_detail(url, {})
    # print json.dumps(detail_info, encoding='UTF-8', ensure_ascii=False)
