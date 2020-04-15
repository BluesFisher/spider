#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
reload(sys)
sys.setdefaultencoding('utf8')

from common.request import Request
from common.utils import Utils
from bs4 import BeautifulSoup
import time
import json
import re

NO_IMG = [
    'http://files.eduuu.com/img/2018/03/07/111547_5a9f59633b91a.jpg',
    'http://gaokaobang.oss-cn-beijing.aliyuncs.com/attachs/img/2019/05/16/120656_5cdce1e052934.jpg'
]


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
        desc_class = 'intro' if mod == 'college_info' else 'desc'
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
                    'class': desc_class
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

    def get_news_detail(self, url, detail_info):

        try:
            res = Request().set_request(url)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")
            content = soup.find('div', {'class': 'main'}).contents

            if 'title' not in detail_info or 'desc' not in detail_info:
                header = soup.find('div', {'class': 'content'})
                h1 = header.find('h1').get_text().strip()
                detail_info['title'] = h1
                detail_info['desc'] = h1
                detail_info['date'] = header.find('span').get_text().strip()

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
                        if img.get('src') not in NO_IMG:
                            img_url = Utils().savePic(img.get('src'))
                            result.append({'img': img_url})
                    continue

                info = re.sub(r'[<br><br/></br>]', '\n',
                              item.get_text().strip()).replace(
                                  '\r', '').replace('\t', '').replace(
                                      '\n\n',
                                      '\n').replace(' ',
                                                    '').replace('[阅读全文]', '')
                if "最新高考资讯、高考政策、考前准备、高考预测、志愿填报、录取分数线等" not in info and '尽在\"高考网\"微信公众号' not in info:
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

    def get_student_guide(self,
                          url,
                          list_items,
                          detail_info={},
                          mod='student_guide'):
        send_url = self.request.get_url(url, mod)

        try:
            res = Request().set_request(send_url)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find_all('table')

            for table in dom:
                tbody = table.find_all('tr')

                for tr in tbody[1:]:  # 第一行为表头
                    td = tr.find_all('td')
                    college_name = td[0].get_text().strip()
                    college_guide = '' if len(td) <= 1 or (
                        not td[1].find('a')) else td[1].find('a')['href']
                    if college_name:
                        list_items[college_name] = {'url': college_guide}

            print 'ok: ', send_url
        except IOError:
            print 'failed: ', send_url
        finally:
            print json.dumps(list_items, encoding='UTF-8', ensure_ascii=False)
            time.sleep(5)
            return list_items, detail_info
