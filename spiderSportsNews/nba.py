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
    url = 'https://china.nba.cn/cms/v1/news/list?column_id=13&last_id=0&page_num=20'
    id_list = CommonFunc().get_nba_news_list(url, [])
    return id_list


def get_news_info(url, file_dict):
    # print 'get_nba_news_detail: ', url

    return CommonFunc().get_nba_news_detail(url, file_dict)

    # print json.dumps(file_dict, encoding='UTF-8', ensure_ascii=False)


def trans_dict_to_arr(file_dict, file_path):
    keys = map(lambda x: int(x), file_dict.keys())
    keys.sort()

    list_file = []

    for i in keys:
        list_file.append(file_dict[str(i)])
    JsonFunc().save_json(list_file, file_path)


def get_news(url_list):
    file_path = PATH + '/nba_news'
    global file_dict

    with open(file_path + '.json') as fp:
        data = fp.read()
        file_dict = eval(data)

    for url in url_list:
        aimUrl = 'https://china.nba.cn/cms/v1/news/info?news_id=' + url
        file_dict = get_news_info(aimUrl, file_dict)
    JsonFunc().save_json(file_dict, file_path)

if __name__ == '__main__':
    url_list = get_news_list()
    print url_list
    get_news(url_list[::-1])
