#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
reload(sys)
sys.setdefaultencoding('utf8')

from common.request import Request
from bs4 import BeautifulSoup
import time
import json
import re


class CommonFunc(object):
    def __init__(self):
        self.request = Request()
        pass

    def get_college_info(self,
                         url,
                         list_items,
                         detail_info={},
                         mod='college_info'):
        send_url = self.request.get_url(url, mod)

        try:
            res = Request().set_request(send_url)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find('ul', {'class': 'text_list1'})
            article_list = dom.find_all('li')

            for li in article_list:
                url = li.find('a')['href'].strip()
                title = li.find_all('a')[0].get_text().strip()
                date = li.find_all('span')[0].get_text().strip()
                desc = li.find('div', {
                    'class': 'intro'
                }).get_text().strip().replace(' ', '')

                info = {
                    'url': url,
                    'title': title,
                    'date': date,
                    'desc': re.sub(r'[\r\n\t]', '', desc)
                }
                list_items.append(info)

            print 'ok: ', send_url
        except IOError:
            print 'failed: ', send_url
        finally:
            print json.dumps(list_items, encoding='UTF-8', ensure_ascii=False)
            time.sleep(5)
            return list_items, detail_info

    def get_college_info_detail(self, url, detail_info):

        try:
            res = Request().set_request(url)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")
            content = soup.find('div', {'class': 'main'}).contents

            result = []

            for item in filter(lambda x: x != '\n', content):
                if item.find('tbody'):
                    thead = []
                    if item.find('thead'):
                        thead = item.find('thead').get_text().split('\n')
                        thead = filter(lambda x: x != '', thead)

                    tbody = []
                    if item.find('tbody'):
                        for tr in item.find('tbody').find_all('tr'):
                            tr_info = tr.get_text().replace(
                                '\r\n', '').replace('\t', '').split('\n')
                            tbody.append(filter(lambda x: x != '', tr_info))

                    result.append({'thead': thead, 'tbody': tbody})
                    continue

                if item.find('img'):
                    for img in item.find_all('img'):
                        if img.get(
                                'src'
                        ) != 'http://gaokaobang.oss-cn-beijing.aliyuncs.com/attachs/img/2019/05/16/120656_5cdce1e052934.jpg':
                            result.append({'img': img.get('src')})
                    continue

                info = re.sub(r'[<br><br/></br>]', '\n',
                              item.get_text().strip()).replace(
                                  '\r', '').replace('\t', '').replace(
                                      '\n\n', '\n').replace(' ', '')
                if "最新高考资讯、高考政策、考前准备、高考预测、志愿填报、录取分数线等" not in info:
                    if item.find('a'):
                        result.append({'a': item.find('a')['href'], 'p': info})
                    else:
                        result.append({'p': info})

            detail_info['content'] = result
            print 'ok: ', url
        except IOError:
            detail_info['content'] = ['failed']
            print 'failed: ', url
        finally:
            time.sleep(5)
            return detail_info
