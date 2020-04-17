#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)

import time
import json
from common.json_func import JsonFunc
from common.utils import Utils
from common_func import CommonFunc

reload(sys)
sys.setdefaultencoding('utf8')

list_items = {}
detail_info = {}
name = ''
failed_item_dict = {}
PATH = PAR_DIR + '/data/profession'


def get_info():
    global list_items
    global detail_info
    with open(PATH + '/result/failed.json') as fp:
        data = fp.read()
        result = Utils().unicode_convert(json.loads(data))
        failed_item_dict = eval(result)

        for item in failed_item_dict.values():
            itemDict = eval(item)
            try:
                list_items, detail_info = CommonFunc().get_pro_info(
                    itemDict['url'], list_items, itemDict)
            except IOError:
                time.sleep(5)
                pass

    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    JsonFunc().save_json(list_items,
                         PATH + '/profile/profession_failed_' + date)
    list_items = {}


if __name__ == '__main__':
    get_info()
