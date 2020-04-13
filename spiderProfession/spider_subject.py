#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append('..')

from common.request import Request
from common.json_func import JsonFunc
from bs4 import BeautifulSoup
import json
import time

reload(sys)
sys.setdefaultencoding('utf8')

START_NUM = 71
END_NUM = 82

list_item = {}
detail_info = {}
name = ''
request = Request()


def get_proInfo(url, detail_info):
    global list_item
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
        list_item["failed_" + url] = detail_info
    finally:
        print json.dumps({name: detail_info},
                         encoding='UTF-8',
                         ensure_ascii=False)
        list_item[name] = detail_info
        time.sleep(5)
        pass


def get_info(start_num, end_num):
    global list_item
    for num in range(start_num, end_num + 1):
        url = 'http://college.gaokao.com/spelist/p' + str(num) + '/'
        itemLink = ''
        try:
            res = request.set_request(url)
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find('div', {'class': 'scores_List'})
            listItem = dom.find_all('dl')

            print 'ok: ', url
            for item in listItem:
                # 专业链接
                itemLink = item.find_all('a')[0]['href']
                detail_info = {"p": num}
                for subItem in item.find_all('li'):
                    info = subItem.get_text().strip().split('：')
                    detail_info[info[0]] = info[1]
                try:
                    get_proInfo(itemLink, detail_info)
                except IOError:
                    time.sleep(5)
                    pass
        except IOError:
            print 'failed: ', url
        finally:
            json_func = JsonFunc()
            json_func.save_json(list_item, './profile/profession_' + str(num))
            list_item = {}
            time.sleep(30)
            pass


if __name__ == '__main__':
    get_info(START_NUM, END_NUM)
    # html = set_request('http://ip.chinaz.com/')
    # html=BeautifulSoup(html.text,"html.parser")
    # html=html.select('.getlist')
    # print(html)
