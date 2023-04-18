#!/usr/bin/python
# -*- coding: UTF-8 -*-

from common_func import CommonFunc
from common.json_func import JsonFunc
from bs4 import element
from bs4 import BeautifulSoup
from common.request import Request
import urllib
import time
import os
import sys

PAR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PAR_DIR)
reload(sys)
sys.setdefaultencoding('utf8')

# import json

PATH = PAR_DIR + '/data/sportsNews'
file_path = PATH + '/fiba_rules'

def get_rule_list(url, class_name, index):
    try:
        file_items = []
        res = Request().set_request(url)

        if res.status_code == 404:
            print 'failed: ', url
            return

        soup = BeautifulSoup(res.text, "html.parser")
        url_list = soup.find('ul', class_=class_name).contents

        for i in range(len(url_list)):
          item = url_list[i]
          if item != None and item != '\n':
              a = item.find('a')
              if 'href' in a.attrs:
                  path = a.attrs['href']
                  file_items.append({ 'id': int(index + str(i)), 'title': a.string, 'path': path })
            
        print 'get_rule_list ok: ', url
    except IOError:
        print 'get_rule_list failed: ', url
    finally:
        return file_items
    
def get_text(text):
   return text.replace(' ', '').replace('    ', '')

def deal_item(item):
    items = []
    for p in item.contents:
      if  p.name == 'p' and (p.text or p.find('img')):
        span = p.find('span') 
        if len(p.find_all('span')) > 2:
            text = get_text(p.text)
            if text != '':
              items.append({ "type": "p", "value": text })
        elif span != None and ('background-color: rgb(255, 255, 0)' not in span.attrs['style'] and 'line-through' not in span.attrs['style']) and span.text !='·':
            if 'line-through' not in span.attrs['style']:
              if 'color: rgb' in span.attrs['style']:
                  text = get_text(span.text)

                  if text != '':
                    items.append({ "type": "p", "value": text, "fontWeight": 800 })

                  if p.text:
                    text = get_text(p.text.replace(text, '').replace(' ', ''))
                    if text != '':
                      items.append({ "type": "p", "value": text })
              else:
                  text = get_text(span.text)
                  if text != '':
                    items.append({ "type": "p", "value": text })
        elif p.find('img'):
            items.append({ "type": "img", "value": p.find('img').attrs['src'] })
        else:
            text = get_text(p.text)
            if text != '':
              items.append({ "type": "p", "value": text })
      elif p.name == 'ul':
        for v in p.find_all('li'):
          text = get_text(v.text)
          if text != '':
            items.append({ "type": "p", "value": text })

    return items

def get_fiba_rule_detail(url):
    try:
        items = []
        res = Request().set_request(url)

        if res.status_code == 404:
            print 'failed: ', url
            return

        soup = BeautifulSoup(res.text, "html.parser")
        contents = soup.find('div', class_='sw-modBox').contents

        for item in contents:
            if item.name == None or type(item.string) == element.Comment or item.name == 'script' or (item.attrs and 'class' in item.attrs and ('bdsharebuttonbox' in item.attrs['class'] or 'mt15' in item.attrs['class'])):
                continue
            
            if 'class' in item.attrs and 'clearfix' in item.attrs['class']:
              items.append({"type": "title", "value": item.find('h1').text})
              items.append({"type": "auth", "value": '中国篮协 | 篮球规则2020'})
            else:
              items = items + deal_item(item.find('p'))
              

    except IOError:
        print 'get_fiba_rule_detail failed: ', url
    finally:
        time.sleep(5)
        return items
    
def get_fiba_rules(url_src = ''):
    fiba_data = get_fiba_data()
    url_list = [{ "path": url_src, 'title': url_src, 'id': 0 }]

    if not url_src:
      # url = 'http://www.lanqiucaipan.com/a/1' # 1
      # url = 'http://www.lanqiucaipan.com/a/52' # 2
      url = 'http://www.lanqiucaipan.com/a/51' # 3
      url_list = get_rule_list(url, 'phpmyfaq_ul', '3')
      fiba_data['urlList'] = url_list
      fiba_data['detailList'] = {}
      JsonFunc().save_json(fiba_data, file_path)

    for i in range(len(url_list)):
        url = url_list[i]
        result = get_fiba_rule_detail(url['path'])
        index = str(url['id'])
        fiba_data['detailList'][index] = result
        JsonFunc().save_json(fiba_data, file_path)
        print 'save ok:', url['title']

def get_fiba_data():
    fiba_data = {}
    with open(file_path + '.json') as fp:
        data = fp.read()
        fiba_data = eval(data)

    return fiba_data


if __name__ == '__main__':
    get_fiba_rules()
    
