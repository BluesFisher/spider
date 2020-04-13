#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


class JsonFunc(object):
    def __init__(self):
        pass

    def save_json(self, items, fileName):
        getDic = json.dumps(items, encoding='UTF-8', ensure_ascii=False)

        # 保存结果JSON
        with open(fileName + '.json', 'w') as json_file:
            json_file.write(getDic)
        json_file.close()
