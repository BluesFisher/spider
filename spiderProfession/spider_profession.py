#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append('..')

import time
import json
from common.request import Request
from common.json_func import JsonFunc
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

START_NUM = 92
END_NUM = 93

list_items = {}
request = Request()


def get_info(start_num, end_num):
    for num in range(start_num, end_num + 1):
        url = 'http://college.gaokao.com/speciality/' + str(num) + '/'
        detailInfo = {"id": num}
        try:
            res = request.set_request(url)
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
        except IOError:
            print 'failed: ', url
        finally:
            print json.dumps({name: detailInfo},
                             encoding='UTF-8',
                             ensure_ascii=False)
            list_items[name] = detailInfo
            time.sleep(5)
            pass


if __name__ == '__main__':
    get_info(START_NUM, END_NUM)
    JsonFunc().save_json(list_items, './profession_detail_' + str(END_NUM))
    list_items = {}
