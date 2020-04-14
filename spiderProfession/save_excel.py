#!/usr/bin/python
# -*-coding:utf-8-*-

import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)

import json
import xlwt
import time
from common.utils import Utils
from common.json_func import JsonFunc

reload(sys)
sys.setdefaultencoding('utf8')

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
profession_files = []
profession_dict = {}
failed_item = {}
json_func = JsonFunc()
utils = Utils()

for root, dirs, files in os.walk(PATH + '/profile'):
    for file in files:
        path = os.path.join(root, file).decode('gbk').encode('utf-8')
        if 'json' in path and 'profession_' in path:
            profession_files.append(path)

# print profession_files
profession_files.append(PATH + '/profile/profession_failed.json')

for path in profession_files:
    with open(path) as fp:
        data = fp.read()
        result = utils.unicode_convert(json.loads(data))

        if len(profession_dict.keys()) == 0:
            profession_dict = eval(result)
        else:
            profession_dict = utils.merge_two_dicts(profession_dict,
                                                    eval(result))

profession_dict = eval(utils.unicode_convert(profession_dict))

for key in profession_dict.copy():
    if 'failed' in key:
        failed_item[key] = profession_dict[key]
        profession_dict.pop(key)

json_func.save_json(profession_dict, PATH + '/result/allProfession')
json_func.save_json(failed_item, PATH + '/result/failed')

# print profession_dict


def saveExcel():
    global profession_dict
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('专业大全', cell_overwrite_ok=True)

    excel_header = [
        '专业', '专业代码', '门类', '学科', '授予学位', '学历层次', '相近专业', '开设高校数量', '主要课程',
        '主干学科', '教学实践', '培养要求', '培养目标', '就业方向', 'url', 'p'
    ]
    for index in range(len(excel_header)):
        sheet.write(0, index, excel_header[index].decode('utf-8'))

    row = 1

    for key in profession_dict:
        sheet.write(row, 0, key.decode('utf-8'))
        value = eval(profession_dict[key])
        # print profession_dict[key]
        for index in range(1, len(excel_header)):
            detail = value[excel_header[index]].replace(" ", '')
            if (excel_header[index] == '相近专业'):
                detail = value[excel_header[index]].strip().replace(
                    " ", '、').replace('.', '')
            elif (excel_header[index] == '开设高校数量'):
                detail = value[excel_header[index]].strip().replace("所", '')
                if not detail:
                    detail = '0'
            sheet.write(row, index, detail.decode('utf-8'))
        row += 1

    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    book.save(PATH + '/result/profession_' + date + '.xls')


saveExcel()
