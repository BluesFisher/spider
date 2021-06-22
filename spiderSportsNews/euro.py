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

URL = [
    # '20210621A07WGV00', 'VNS2021062100524000', 'ICT2021062100378000',
    # 'SPO2021062100490200', '20210621A04J0L00', '90QV1JVFT256301U100',
    # '20210621A04YEP00', '90QV1J24T25631P5100', '20210621A02WWB00',
    # '90QV1NN3T25632UQ100'
    '20210622A00LTR00',
    '20210622A00FXO00',
    '20210622A00LZZ00',
    '20210622A00K3J00',
    '20210622A00F8400',
    '20210622A00FAT00',
    '20210622A00N7H00',
    '20210622A00N7C00',
    '20210622A00FT900',
    '20210622A00LX700'
]

# URL = [
#     'VNS2021062100524000', 'ICT2021062100378000', '90QV1JVFT256301U100',
#     '90QV1J24T25631P5100', '90QV1NN3T25632UQ100'
# ]


def get_news_list():
    url = 'https://xw.qq.com/zt/20210519008860/SPO20210519008860FR'
    id_list = CommonFunc().get_news_list(url, [])
    print id_list


def get_news_info(url, file_dict):
    print 'get_news_info: ', url

    return CommonFunc().get_news_detail(url, file_dict)

    # print json.dumps(file_dict, encoding='UTF-8', ensure_ascii=False)


def get_news():
    file_path = PATH + '/euro_news'
    global file_dict

    with open(file_path + '.json') as fp:
        data = fp.read()
        file_dict = eval(data)

    for url in URL:
        aimUrl = 'https://xw.qq.com/cmsid/' + url
        file_dict = get_news_info(aimUrl, file_dict)
    JsonFunc().save_json(file_dict, file_path)


if __name__ == '__main__':
    # get_news_list()
    get_news()
