#!/usr/bin/env python3
# -*- conding: utf-8 -*-
# Description: get text info from html and save to local file

import requests
import logging as log
import sys
import os
import io
import re

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    log.info('获取网页源代码...')
    res = requests.get(url, headers=headers, timeout=20)

    if res.status_code != 200:
        log.error('get failed, status code:{}'.format(res.status_code))
        return None

    return BeautifulSoup(res.content, 'lxml')


def common_parse(article):
    text = article.find_all(text=True)
    output = []
    tag_blacklist = ['[document]', 'html', 'head', 'meta', 'body', 'header',
                     'nav', 'script', 'footer', 'noscript', 'input', 'style']

    for t in text:
        if not t.strip() or t.parent.name in tag_blacklist:
            continue
        output.append('{}'.format(t))

    return '\n'.join(output)


def whitelist_parse(html, cls):
    """Parse specific websites"""
    article = html.find('div', {'class': cls})

    if not article:
        log.error('未从当前白名单网页中找到有效信息！\n')
        return None

    return common_parse(article)


def save(output):
    save_dir = 'results'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_name = '{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    file_path = os.path.join(save_dir, file_name)
    with io.open(file_path, 'w', newline='\r\n', encoding='utf-8') as f:
        f.write(output)

    log.info('文档已保存至\"{}\".\n'.format(file_path))
    try:
        os.system('notepad.exe {}'.format(file_path))
    finally:
        pass


# specific websites
web_whitelist = {
    'www.upkao.com': 'm-cmsinfo-cont',
    'www.ycykyl.com': 'showren',
    'www.zuowen.com': 'con_content',
}

def download(url):
    html = get_html(url)
    if not html:
        return

    web_domain = urlparse(url).netloc
    log.info('获取网站域名: {}'.format(web_domain))

    if web_domain in web_whitelist:
        log.info('网站域名 {} 在当前白名单中'.format(web_domain))
        output = whitelist_parse(html, web_whitelist[web_domain])
    else:
        output = common_parse(html)

    if output:
        save(output)


def destroy(code):
    print('###########################################\n'
          '# 欢迎下次使用哦，我的增宝宝  ----litreiy #\n'
          '###########################################\n')
    input('Press ENTER to exit')
    sys.exit(code)


def main():
    print('###########################################\n'
          '# 给我增宝宝的专属脚本        ----litreiy #\n'
          '###########################################\n')
    log.basicConfig(format='[%(levelname)s] %(message)s', level=log.INFO)
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                         '(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    try:
        while True:
            url = input("请输入要解析的网址(exit退出)：")
            if url == 'exit':
                destroy(0)
            elif not url:
                continue
            elif not re.findall(pattern, url):
                log.warn('网址\"{}\" 无效.'.format(url))
                continue

            download(url)
    except KeyboardInterrupt as ki:
        print('\n按键中断，已强制退出！')
        destroy(0)

if __name__ == '__main__':
    main()

