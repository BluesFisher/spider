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

NO_IMG = [
    'http://files.eduuu.com/img/2018/03/07/111547_5a9f59633b91a.jpg',
    'http://gaokaobang.oss-cn-beijing.aliyuncs.com/attachs/img/2019/05/16/120656_5cdce1e052934.jpg'
]


class CommonFunc(object):
    def __init__(self):
        self.request = Request()
        pass

    def get_college_detail(self,
                           url,
                           list_items,
                           detail_info={},
                           mod='college_detail'):
        send_url = self.request.get_url(url, mod)

        try:
            res = Request().set_request(send_url)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, "html.parser")

            dom = soup.find('div', {'class': 'scores_List'})
            dl = dom.find_all('dl')

            for dl_item in dl:
                dt = dl_item.find('dt')
                college_name = dt.get_text().strip()

                if college_name in list_items:
                    continue

                img = dt.find('img').get('src')
                img_url = Utils().savePic(img,
                                          path_in='logo/' + college_name + '-')

                list_items[college_name] = {'logo': img_url}

            print 'ok: ', send_url, len(dl)
        except IOError:
            print 'failed: ', send_url
        finally:
            print json.dumps(list_items, encoding='UTF-8', ensure_ascii=False)
            time.sleep(5)
            return list_items, detail_info
