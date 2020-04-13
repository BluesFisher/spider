#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time
import json
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')


listItems = {}

# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
# }

proxyList = [
    '221.122.91.66:80'
    # '59.62.7.186:9000',
    # '27.214.50.175:9000',
    # '223.241.117.120:8010',
    # '27.220.121.211:9000',
    # '27.220.120.142:9000'
]

detailInfo = {}
name = ''
failedItemDict = {}


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


def get_header():
    location = os.getcwd() + '/fake_useragent.json'
    ua = UserAgent(path=location)
    return ua.random


def setRequest(url):
    # proxy = { 'http': 'http://' + proxyList[random.randint(0,len(proxyList) - 1)] }
    headers = {'user-agent': get_header()}
    # print proxy, headers
    # res = requests.get(url, headers=headers, proxies=proxy)
    res = requests.get(url, headers=headers)

    return res


def getProInfo(url, detailInfo):
    global listItems
    detailInfo["url"] = url
    try:
        res = setRequest(url)
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
            temp = item.get_text().strip().split('\r\n')
            # print name, json.dumps(temp, encoding='UTF-8', ensure_ascii=False)
            if len(temp) > 1:
                detailInfo[temp[0].strip()] = temp[1].strip().strip(
                    '\r').strip('\n')
            else:
                detailInfo[temp[0].strip()] = ''

        print 'ok: ', url
    except:
        print 'failed: ', url
        listItems["failed_" + url] = detailInfo
    finally:
        print json.dumps({name: detailInfo},
                         encoding='UTF-8', ensure_ascii=False)
        listItems[name] = detailInfo
        time.sleep(5)
        pass


def saveJson(num):
    global listItems
    getDic = json.dumps(listItems, encoding='UTF-8', ensure_ascii=False)
    # print getDic

    # 保存结果JSON
    with open('./profile/profession_' + str(num) + '_' + str(int(time.time())) + '.json', 'w') as json_file:
        json_file.write(getDic)
    json_file.close()

    listItems = {}


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def getInfo():
    global listItems
    with open('./failed.json') as fp:
        data = fp.read()
        result = unicode_convert(json.loads(data))
        failedItemDict = eval(result)

        for item in failedItemDict.values()[0:1]:
            itemDict = eval(item)
            try:
                getProInfo(itemDict['url'], itemDict)
            except:
                time.sleep(5)
                pass

    saveJson('failed')


if __name__ == '__main__':
    getInfo()
