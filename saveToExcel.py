#!/usr/bin/python
# -*-coding:utf-8-*-

import shutil
import os
import json
import sys
import xlwt
import time

reload(sys)
sys.setdefaultencoding('utf8')

professionFiles = []
professionDict = {}
failedItem = {}


def unicode_convert(input):
    result = ''
    if isinstance(input, dict):
        result = {unicode_convert(key): unicode_convert(value)
                  for key, value in input.iteritems()}
    elif isinstance(input, list):
        result = [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        result = input.encode('utf-8')
    else:
        result = input
    return str(result).decode("string_escape")


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def saveJson(item, name):
    getDic = json.dumps(item, encoding='UTF-8', ensure_ascii=False)

    with open('./' + name, 'w') as json_file:
        json_file.write(getDic)
    json_file.close()


for root, dirs, files in os.walk('./profile'):
    for file in files:
        path = os.path.join(root, file).decode('gbk').encode('utf-8')
        if 'json' in path and 'profession_' in path:
            professionFiles.append(path)

# print professionFiles
professionFiles.append('./profile/profession_failed.json')

for path in professionFiles:
    with open(path) as fp:
        data = fp.read()
        result = unicode_convert(json.loads(data))

        if len(professionDict.keys()) == 0:
            professionDict = eval(result)
        else:
            professionDict = merge_two_dicts(professionDict, eval(result))

professionDict = eval(unicode_convert(professionDict))

for key in professionDict.copy():
    if 'failed' in key:
        failedItem[key] = professionDict[key]
        professionDict.pop(key)

saveJson(professionDict, 'allProfession.json')
saveJson(failedItem, 'failed.json')

# print professionDict


def saveExcel():
    global professionDict
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('专业大全', cell_overwrite_ok=True)

    excelHeader = ['专业', '专业代码', '门类', '学科', '授予学位', '学历层次', '相近专业',
                   '开设高校数量', '主要课程', '主干学科', '教学实践', '培养要求', '培养目标', '就业方向', 'url', 'p']
    for index in range(len(excelHeader)):
        sheet.write(0, index, excelHeader[index].decode('utf-8'))

    row = 1

    for key in professionDict:
        sheet.write(row, 0, key.decode('utf-8'))
        value = eval(professionDict[key])
        # print professionDict[key]
        for index in range(1, len(excelHeader)):
            detail = value[excelHeader[index]].replace(" ", '')
            if (excelHeader[index] == '相近专业'):
                detail = value[excelHeader[index]].strip().replace(
                    " ", '、').replace('.', '')
            elif (excelHeader[index] == '开设高校数量'):
                detail = value[excelHeader[index]].strip().replace("所", '')
                if not detail:
                    detail = '0'
            sheet.write(row, index, detail.decode('utf-8'))
        row += 1

    date = time.strftime('%m%d', time.localtime(time.time()))
    book.save('profession_' + date + '.xls')


saveExcel()
