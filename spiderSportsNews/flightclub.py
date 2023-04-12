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

file_dict = []
PATH = PAR_DIR + '/data/sportsNews'


def get_news_info(url):
    return get_flightclub_detail(url)

def parse_flight(contents):
    res = []
    for item in contents:
        item_soup = BeautifulSoup(str(item), "html.parser").contents
        if len(item_soup) > 1:
            res_item = parse_flight(item_soup)
            res = res + res_item
        elif item.name == 'img':
            img_src = ''
            if 'data-original' in item.attrs:
                img_src = item.attrs['data-original']
            else:
                img_src = item.attrs['src']
            
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            res.append({ "type": "img", "value": img_src })
        elif item.name == 'strong':
            res.append({ "type": "p", "value": item.string, "fontWeight": 800 })
        elif item.name == None and (item.string != '\n') and  (type(item.string) != element.Comment):
            p = item.string.replace('\n', '').replace('\r', '').replace('\t', '')
            if p != '' and p != ' ':
              res.append({ "type": "p", "value": p})
        elif item.name != None and item.name.startswith('h'):
            string = item.text.replace('\n', '').replace('\r', '，')
            res.append({ "type": "p", "value": string, "fontWeight": 800 }) 
    return res


def get_flightclub_detail(url):
    try:
        items = [{"type": "tag", "className": "tag-red-7", "value": "球鞋"}]
        res = Request().set_request(url)

        if res.status_code == 404:
            print 'failed: ', url
            return

        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find('div', class_='news_title').find('h1').text
        items.append({"type": "title", "value": title})
        pub_time = soup.find('div', class_='news_info left pure-u-1 pure-u-md-4-24').find(
            'div', class_='body').div.text.split(' ')[0]
        items.append({"type": "auth", "value": "FLIGHTCLUB中文站 | " + pub_time})

        contents = soup.find('div', class_='content').contents
        items = items + parse_flight(contents)
    except IOError:
        print 'get_flightclub_detail failed: ', url
    finally:
        time.sleep(5)
        return items


def get_news_list(url):
    try:
        file_items = []
        res = Request().set_request(url)

        if res.status_code == 404:
            print 'failed: ', url
            return

        soup = BeautifulSoup(res.text, "html.parser")
        url_list = soup.find_all('div', class_='news_item normal pure-g')

        for item in url_list:
            path = item.find('a').attrs['href']
            file_items.append('https://www.flightclub.cn' + path)

        print 'get_news_list ok: ', url
    except IOError:
        print 'get_news_list failed: ', url
    finally:
        return file_items


def get_news():
    file_path = PATH + '/flightclub'
    file_got_path = PATH + '/flightclub_path'
    search_key = urllib.quote('詹姆斯') # 科比
    search_url = 'https://www.flightclub.cn/sneaker/search/' + search_key
    file_items = []
    flie_got = []
  
    with open(file_path + '.json') as fp:
        data = fp.read()
        file_items = eval(data)

    with open(file_got_path + '.json') as fp:
        data = fp.read()
        flie_got = eval(data)

    for i in range(2):
        index = i * 20
        indexStr = '' if index == 0 else ('/' + str(index))
        url_list = get_news_list(search_url + indexStr)
        for url in url_list:
            if url not in flie_got:
              res = get_news_info(url)
              file_items.append(res)
              JsonFunc().save_json(file_items, file_path)
          
              flie_got.append(url)
              JsonFunc().save_json(flie_got, file_got_path)
            else:
              print 'repeat: ', url  


if __name__ == '__main__':
    get_news()
