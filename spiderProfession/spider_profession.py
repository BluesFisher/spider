#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)

from common.json_func import JsonFunc
from common_func import CommonFunc

reload(sys)
sys.setdefaultencoding('utf8')

START_NUM = 92
END_NUM = 92

list_items = {}
PATH = PAR_DIR + '/data/profession'


def get_info(start_num, end_num):
    global list_items
    for num in range(start_num, end_num + 1):
        url = str(num) + '/'
        detail_info = {"id": num}

        list_items, detail_info = CommonFunc().get_pro_info(
            url, list_items, detail_info)


if __name__ == '__main__':

    get_info(START_NUM, END_NUM)
    JsonFunc().save_json(list_items,
                         PATH + '/profession_detail_' + str(END_NUM))
    list_items = {}
