#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Utils(object):
    def __init__(self):
        self.url = {
            'pro_list_url': 'http://college.gaokao.com/spelist/',
            'pro_url': 'http://college.gaokao.com/speciality/'
        }
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
