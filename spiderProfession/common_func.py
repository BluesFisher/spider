#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from common.request import Request
from bs4 import BeautifulSoup
import time
import json


class CommonFunc(object):
    def __init__(self):
        self.request = Request()
        pass

    def get_pro_info(self, url, list_items, detail_info, mod='pro_url'):
        send_url = self.request.get_url(url, mod)
        detail_info["url"] = send_url
        name = ''

        try:
            res = Request().set_request(send_url)
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

            print 'ok: ', send_url
        except IOError:
            print 'failed: ', send_url
            list_items["failed_" + send_url] = detail_info
        finally:
            print json.dumps({name: detail_info},
                             encoding='UTF-8',
                             ensure_ascii=False)
            list_items[name] = detail_info
            time.sleep(5)
            return list_items, detail_info
