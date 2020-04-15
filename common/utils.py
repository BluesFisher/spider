#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import uuid
import time
from common import PROFESSION_UA_PATH


class Utils(object):
    def __init__(self):
        pass

    def unicode_convert(self, input):
        result = ''
        if isinstance(input, dict):
            result = {
                self.unicode_convert(key): self.unicode_convert(value)
                for key, value in input.iteritems()
            }
        elif isinstance(input, list):
            result = [self.unicode_convert(element) for element in input]
        elif isinstance(input, unicode):
            result = input.encode('utf-8')
        else:
            result = input
        return str(result).decode("string_escape")

    def merge_two_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    def savePic(self, url, path_in=''):
        if not url:
            return ''
        try:
            if 'icon_default' in url:
                return PROFESSION_UA_PATH['static'] + path_in + 'none.png'

            imgres = requests.get(url)  # 取得文件内容

            if imgres.status_code == 404:
                return PROFESSION_UA_PATH['static'] + path_in + 'none.png'

            path = PROFESSION_UA_PATH['static'] + path_in + str(
                uuid.uuid4()) + '.png'
            with open(path, "wb") as f:
                f.write(imgres.content)
            time.sleep(5)
            return path
        except IOError:
            return url
