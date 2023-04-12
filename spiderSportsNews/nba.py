#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import datetime

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)
reload(sys)
sys.setdefaultencoding('utf8')

# import json
from common.json_func import JsonFunc
from common_func import CommonFunc

file_dict = []
img_index = 1
date_format = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
PATH = PAR_DIR + '/data/sportsNews'
IMG_ROOT_PATH = PATH + '/nbaPic/' + date_format +  '/'

os.makedirs(IMG_ROOT_PATH)

def get_news_list():
    url = 'https://china.nba.cn/cms/v1/news/list?column_id=13&last_id=0&page_num=20&page_size=20'
    id_list = CommonFunc().get_nba_news_list(url, [])
    return id_list


def get_news_info(url, file_dict):
    return CommonFunc().get_nba_news_detail(url, file_dict)


def trans_dict_to_arr(file_dict, file_path):
    keys = map(lambda x: int(x), file_dict.keys())
    keys.sort()

    list_file = []

    for i in keys:
        list_file.append(file_dict[str(i)])
    JsonFunc().save_json(list_file, file_path)

def save_img(url):
    global img_index

    if not url:
        return
    
    img_path = IMG_ROOT_PATH + str(img_index) + '.jpg'
    img = CommonFunc().get_network_img(url)
    read_path = '/nbaJson/pic/news/' + date_format + '/'

    with open(img_path, 'wb') as fp:
        fp.write(img)
        img_index = img_index + 1

    return read_path + str(img_index - 1) + '.jpg'


def get_news(url_list):
    file_path = PATH + '/nba_news'
    global file_dict

    # with open(file_path + '.json') as fp:
    #     data = fp.read()
    #     file_dict = eval(data)
    
    file_dict = []

    for url in [url_list[0]]:
        aimUrl = 'https://china.nba.cn/cms/v1/news/info?news_id=' + url
        file_dict = get_news_info(aimUrl, file_dict)

    for item in file_dict:
        for v in item:
            if v['type'] == 'img':
                read_path = save_img(v['value'])
                v['value'] = read_path

    JsonFunc().save_json(file_dict, file_path)

if __name__ == '__main__':
    url_list = get_news_list()
    print url_list
    get_news(url_list[::-1])
    print date_format