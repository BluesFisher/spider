#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
reload(sys)
sys.setdefaultencoding('utf8')

from common.request import Request
# from common.utils import Utils
from bs4 import BeautifulSoup
import time
import json
import re


class CommonFunc(object):
    def __init__(self):
        self.request = Request()
        pass

    def get_news_detail(self, url, list_items):
        try:
            file_items = []
            res = Request().set_request(url)
            # res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")
            content = soup.find('script', id='__NEXT_DATA__').contents
            contentJson = json.loads(content[0])
            article = contentJson['props']['pageProps']['data']['data']

            if len(article['json_content']
                   ) == 0 or article['json_content'][0]['type'] == 3:
                print 'no data: ', url
                return list_items

            file_items.append({'type': 'title', 'value': article['title']})
            file_items.append({
                'type':
                'auth',
                'value':
                article['src'] + ' | ' + article['pubtime']
            })

            for item in article['json_content']:
                if item['type'] == 1:
                    info = {'type': 'p', 'value': item['value']}
                    if 'STRONG' in item['value'] or '<h' in item['value']:
                        info['value'] = re.sub(
                            r'<STRONG>|<\/STRONG>|<strong>|<\/strong>|<h2>|<\/h2>|<h1>|<\/h1>',
                            '', item['value'])
                        info['fontWeight'] = 'bold'

                    file_items.append(info)

                if item['type'] == 2:
                    file_items.append({
                        'type': 'img',
                        'value': item['gif'] or item['value']
                    })

            file_items.append({'type': 'p', 'value': '转自腾讯新闻'})

            list_items.append(file_items)

            print 'ok: ', url
        except IOError:
            print 'failed: ', url
        finally:
            time.sleep(5)
            return list_items

    def get_news_list(self, url, list_items):
        try:
            id_list = []
            res = Request().set_request(url)
            print res, res.status_code

            if res.status_code == 404:
                time.sleep(5)
                return self.get_news_list(url, list_items)

            soup = BeautifulSoup(res.text, "html.parser")
            content = soup.find('script', id='__NEXT_DATA__').contents
            contentJson = json.loads(content[0])
            idlist = contentJson['props']['pageProps']['data']['data'][
                'idlist']

            for item in idlist:
                if item['ids']:
                    for id in item['ids']:
                        id_list.append(id['id'])

            list_items = id_list[0:10]

        except IOError:
            list_items = []
            print 'failed: ', url

        time.sleep(5)
        return list_items

    def get_nba_news_list(self, url, list_items):
        try:
            id_list = []
            res = Request().set_request(url)
            contentJson = json.loads(res.text)
            idlist = contentJson['data']

            for item in idlist:
                id_list.append(item['news_id'])

            list_items = id_list

        except IOError:
            list_items = []
            print 'failed: ', url
        finally:
            time.sleep(5)
            return list_items

    def get_nba_news_detail(self, url, list_items):
        try:
            file_items = []
            res = Request().set_request(url)
            # res.encoding = 'gbk'
            contentJson = json.loads(res.text)
            data = contentJson['data']
            cnt_attr = data['cnt_attr']

            if contentJson['code'] != 0 or not data:
                print 'no data: ', url
                return list_items

            file_items.append({'type': 'title', 'value': data['title']})
            file_items.append({
                'type':
                'auth',
                'value':
                data['source'] + ' | ' + data['publish_time']
            })

            for item in cnt_attr:
                detail = json.loads(item['object'])
                if 'IMG_' in item['placeholder']:
                  file_items.append({'type': 'img', 'value': detail['imgurl']})
                if 'TXT_' in item['placeholder']:
                  file_items.append({'type': 'p', 'value': detail['content']})
                if 'VIDEO_' in item['placeholder']:
                  file_items.append({'type': 'img', 'value': detail['image']})

            # html = BeautifulSoup(data['cnt_html'], "html.parser").find_all('p')

            # for item in html:
            #     p = item.get_text()
            #     content = ''.join(map(lambda x: str(x), item.contents))

            #     if p or content:
            #         if 'IMG_' in content:
            #             img = content
            #             file_items.append({
            #                 'type':
            #                 'img',
            #                 'value':
            #                 re.sub(r'http:', 'https:',
            #                        cnt_attr[img]['img']['imgurl0']['imgurl'])
            #             })
            #         else:
            #             info = {
            #                 'type':
            #                 'p',
            #                 'value':
            #                 re.sub(
            #                     r'<STRONG>|<\/STRONG>|<h2>|<\/h2>|<h1>|<\/h1>',
            #                     '', p.lower())
            #             }

            #             if content.lower().startswith(
            #                     '<strong>') and content.lower().endswith(
            #                         '</strong>'):
            #                 info['fontWeight'] = 'bold'
            #             file_items.append(info)

            list_items.append(file_items)

            print 'ok: ', url
        except IOError:
            print 'failed: ', url
        finally:
            time.sleep(5)
            return list_items
