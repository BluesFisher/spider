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

def get_news_info(url):
    # print 'get_nba_news_detail: ', url

    return CommonFunc().get_area_detail(url)

    # print json.dumps(file_dict, encoding='UTF-8', ensure_ascii=False)


def get_news():
    file_path = PATH + '/area'
    save_path = PATH + '/area-res'
    global file_dict
    content = []
    res = []

    with open(file_path + '.json') as fp:
        data = fp.read()
        file_dict = eval(data)

    for index in range(len(file_dict)):
        url = 'https://i.meituan.com/wrapapi/allpoiinfo?riskLevel=71&optimusCode=10&isDaoZong=true&poiId=' + str(file_dict[index]['orgId'])
        res = get_news_info(url)
        file_dict[index]['orgAddr'] = res['address']
        file_dict[index]['phone'] = res['phone']
        file_dict[index]['desc'] = '营业时间：' + res['openTime'].replace('\n', ' ') or '-'
        content.append(file_dict[index])

        print 'ok: ', file_dict[index]['orgId'], index

        if (index > 0 and index % 10 == 0):
            with open(save_path + '.json') as fp:
              data = fp.read()
              res = eval(data)
            JsonFunc().save_json(res + content, save_path)
            content = []
            
    with open(save_path + '.json') as fp:
      data = fp.read()
      res = eval(data)
    JsonFunc().save_json(res + content, save_path)

if __name__ == '__main__':
    get_news()
