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

list_items = {}
detail_info = {}
name = ''
failed_item_dict = {}
request = Request()


def get_pro_info(url, detail_info):
    global list_items
    detail_info["url"] = url
    try:
        res = request.set_request(url)
        soup = BeautifulSoup(res.text, "html.parser")

        dom = soup.find('div', {'class': 'bg_sez'})

        # 专业名称
        name = dom.find_all('h2')[0].get_text().strip()

        # 专业高校数量
        school = dom.find_all('span')[0].get_text().strip().split("：")
        detail_info[school[0]] = school[1]

        # 专业学科
        subject = dom.find('div', {'class': 'xuen_kc'}).find_all('p')
        for item in subject:
            temp = item.get_text().strip().split("：")
            detail_info[temp[0]] = temp[1]

        # 详细介绍
        detail = soup.find('div', {'class': 'tab_con'}).find_all('p')
        for item in detail:
            temp = item.get_text().strip().split('\r\n')
            # print name, json.dumps(temp, encoding='UTF-8', ensure_ascii=False)
            if len(temp) > 1:
                detail_info[temp[0].strip()] = temp[1].strip().strip(
                    '\r').strip('\n')
            else:
                detail_info[temp[0].strip()] = ''

        print 'ok: ', url
    except IOError:
        print 'failed: ', url
        list_items["failed_" + url] = detail_info
    finally:
        print json.dumps({name: detail_info},
                         encoding='UTF-8',
                         ensure_ascii=False)
        list_items[name] = detail_info
        time.sleep(5)
        pass


def get_info():
    global list_items
    with open('./failed.json') as fp:
        data = fp.read()
        result = request.unicode_convert(json.loads(data))
        failed_item_dict = eval(result)

        for item in failed_item_dict.values():
            itemDict = eval(item)
            try:
                get_pro_info(itemDict['url'], itemDict)
            except IOError:
                time.sleep(5)
                pass

    date = time.strftime('%m%d', time.localtime(time.time()))
    JsonFunc().save_json(list_items, './profile/profession_failed_' + date)
    list_items = {}


if __name__ == '__main__':
    get_info()
