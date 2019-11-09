#!/usr/bin/env python3
# -*- conding: utf-8 -*-
# Description: get text info from html and save to local file

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import datetime
import sys
import os
import io


def whitelist_parse(html, cls):
    """Parse specific websites"""
    article = html.find('div', {'class': cls})
    return common_parse(article)


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    res = requests.get(url, headers=headers, timeout=20)

    if res.status_code != 200:
        sys.exit(0)

    return BeautifulSoup(res.content, 'lxml')


def common_parse(article):
    text = article.find_all(text=True)
    output = ''
    count = 0 # count of '\n'
    blacklist = ['[document]', 'html', 'head', 'meta', 'body', 'header',
                 'script', 'a', 'noscript', 'input', 'style']

    for t in text:
        if t.parent.name in blacklist:
            count += 1
            continue

        count = count + 1 if t == '\n' else 0
        if count > 1:
            continue

        output += '{}'.format(t)

    return output


def save(output):
    with io.open('text.txt', 'w', newline='\r\n', encoding='utf-8') as f:
        f.write(output)


web_cls = {
    """parser for specific websites"""
    'www.ycykyl.com': 'showren',
    'www.upkao.com': 'm-cmsinfo-cont',
    'www.zuowen.com': 'con_content',
}

def main():
    url = sys.argv[1]
    html = get_html(url)

    web_domain = urlparse(url).netloc
    print('get domain of website: {}'.format(web_domain))

    if web_domain in web_cls:
        output = whitelist_parse(html, web_cls[web_domain])
    else:
        output = common_parse(html)

    save(output)

if __name__ == '__main__':
    main()
