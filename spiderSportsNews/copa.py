#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)
reload(sys)
sys.setdefaultencoding('utf8')

# import json
from common.json_func import JsonFunc
from common_func import CommonFunc

file_dict = []
PATH = PAR_DIR + '/data/sportsNews'


def get_news_list():
    url = 'https://xw.qq.com/zt/202106130042070/SPO202106130042070K'
    id_list = CommonFunc().get_news_list(url, [])
    return id_list


def get_news_info(url, file_dict):
    print 'get_news_info: ', url

    return CommonFunc().get_news_detail(url, file_dict)

    # print json.dumps(file_dict, encoding='UTF-8', ensure_ascii=False)


def get_news(url_list):
    file_path = PATH + '/copa_news'
    global file_dict

    with open(file_path + '.json') as fp:
        data = fp.read()
        file_dict = eval(data)

    for url in url_list:
        aimUrl = 'https://xw.qq.com/cmsid/' + url
        file_dict = get_news_info(aimUrl, file_dict)
    JsonFunc().save_json(file_dict, file_path)


if __name__ == '__main__':
    url_list = get_news_list()
    print url_list
    get_news(url_list[::-1])
