#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import datetime
import shutil

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
IMG_PIC_DIR = PATH + '/nbaPic/'
IMG_ROOT_PATH = IMG_PIC_DIR + date_format +  '/'
file_got_path = PATH + '/nba_news_path'

try:
    shutil.rmtree(IMG_PIC_DIR)
    os.removedirs(IMG_PIC_DIR)
except:
    print 'removedirs error'
os.makedirs(IMG_PIC_DIR)
os.makedirs(IMG_ROOT_PATH)

def get_news_list():
    url = 'https://china.nba.cn/cms/v1/news/list?column_id=13&last_id=0&page_num=20&page_size=40'
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
    
    file_type = '.gif' if '.gif' in url else '.jpg'
    img_path = IMG_ROOT_PATH + str(img_index) + file_type
    img = CommonFunc().get_network_img(url)
    read_path = '/nbaJson/pic/news/' + date_format + '/'

    with open(img_path, 'wb') as fp:
        fp.write(img)
        img_index = img_index + 1

    return read_path + str(img_index - 1) + file_type

def already_got_news():
    global file_got_path
    flie_got = []

    with open(file_got_path + '.json') as fp:
        data = fp.read()
        flie_got = eval(data)

    return flie_got


def get_news(url_list):
    file_path = PATH + '/nba_news'
    global file_dict
    flie_got = already_got_news()

    # with open(file_path + '.json') as fp:
    #     data = fp.read()
    #     file_dict = eval(data)
    
    file_dict = []

    for url in url_list:
        aimUrl = 'https://china.nba.cn/cms/v1/news/info?news_id=' + url
        file_dict = get_news_info(aimUrl, file_dict)
        last_dict = file_dict[-1]
        last_dict_title = last_dict[0]["value"]
        if last_dict_title not in flie_got:
            for v in last_dict:
                if v['type'] == 'img':
                    read_path = save_img(v['value'])
                    v['value'] = read_path

            JsonFunc().save_json(file_dict, file_path)

            flie_got.append(last_dict_title)
            JsonFunc().save_json(flie_got, file_got_path)
        else:
            file_dict.pop()

    

if __name__ == '__main__':
    url_list = get_news_list()
    print url_list
    get_news(url_list[::-1])
    print date_format