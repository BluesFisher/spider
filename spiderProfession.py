#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import json
import os
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')


listItems = {}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}

startNum = 92
endNum = 200


def getInfo(startNum, endNum):
    for num in range(startNum, endNum + 1):
        url = 'http://college.gaokao.com/speciality/' + str(num) + '/'
        detailInfo = {"id": num}
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find('div', {'class': 'bg_sez'})

            # 专业名称
            name = dom.find_all('h2')[0].get_text().strip()

            # 专业高校数量
            school = dom.find_all('span')[0].get_text().strip().split("：")
            detailInfo[school[0]] = school[1]

            # 专业学科
            subject = dom.find('div', {'class': 'xuen_kc'}).find_all('p')
            for item in subject:
                temp = item.get_text().strip().split("：")
                detailInfo[temp[0]] = temp[1]

            # 详细介绍
            detail = soup.find('div', {'class': 'tab_con'}).find_all('p')
            for item in detail:
                temp = item.get_text().strip().split(' ')
                # print json.dumps(temp, encoding='UTF-8', ensure_ascii=False)
                if len(temp) > 1:
                    detailInfo[temp[0]] = temp[1].strip('\n')
                else:
                    detailInfo[temp[0]] = ''

            print 'ok: ', url
        except:
            print 'failed: ', url
        finally:
            print json.dumps({name: detailInfo},
                             encoding='UTF-8', ensure_ascii=False)
            listItems[name] = detailInfo
            time.sleep(5)
            pass


getInfo(startNum, endNum)

getDic = json.dumps(listItems, encoding='UTF-8', ensure_ascii=False)
# print getDic

# 保存结果JSON
with open('./profession_' + str(endNum) + '.json', 'w') as json_file:
    json_file.write(getDic)
json_file.close()
