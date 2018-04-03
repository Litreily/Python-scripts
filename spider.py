#!/usr/bin/python3
# -*-coding:utf-8-*-

import queue
from threading import Thread

import requests

import re
from bs4 import BeautifulSoup

import os
import platform

# url format ↓
# http://www.cfachina.org/cfainfo/organbaseinfoOneServlet?organid=+G01001+&currentPage=1&pageSize=20&selectType=personinfo&all=undefined
# organid: +G01001+, +G01002+, +G01003+, ...
# currentPage: 1, 2, 3, ...
# pageSize: 20(default)
# 
# Algorithm design:
# 2 threads with 2 queues
# Thread-1, get first page url, then get page_num and mechanism_name from first page
# Thread-2, parse html file and get data from it, then output data to local file
# url_queue data -> 'url'  # first url of each mechanism
# html_queue data -> {'name':'mechanism_name', 'html':data}

url_queue = queue.Queue()
html_queue = queue.Queue()


class SpiderThread(Thread):
    """Threaded Url Grab"""
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue
        self.page_size = 20
        self.url_re = re.compile('#currentPage.*\+.*\+\'(\d+)\'')
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def __get_url(self, mechanism_id, current_page):
        return 'http://www.cfachina.org/cfainfo/organbaseinfoOneServlet?organid=+%s+&currentPage=%d&pageSize=%d&selectType=personinfo&all=undefined' \
        % (mechanism_id, current_page, self.page_size)

    def grab(self, url):
        '''Grab html of url from web'''
        while True:
            try:
                html = requests.get(url, headers=self.headers, timeout=20)
                if html.status_code == 200:
                    break
            except requests.exceptions.ConnectionError as e:
                print(url + ' Connection error, try again...')
            except requests.exceptions.ReadTimeout as e:
                print(url + ' Read timeout, try again...')
            finally:
                pass
        return html
    
    def run(self):
        '''Grab all htmls of mechanism one by one
        Steps:
            1. grab first page of each mechanism from url_queue
            2. get number of pages and mechanism name from first page
            3. grab all html file of each mechanism
            4. push all html to html_queue
        '''
        while True:
            mechanism_id = 'G0' + self.url_queue.get()

            # the first page's url
            url = self.__get_url(mechanism_id, 1)
            html = self.grab(url)

            page_cnt = self.url_re.search(html.text).group(1)
            if page_cnt == '0':
                continue
            
            soup = BeautifulSoup(html.text, 'html.parser')
            mechanism_name = soup.find('', {'class':'gst_title'}).find_all('a')[2].get_text()
            print('\nGrab Thread: get %s - %s with %s pages\n' % (mechanism_id, mechanism_name, page_cnt))

            # put data into html_queue
            self.html_queue.put({'name':'%s_%s' % (mechanism_id, mechanism_name), 'num':1, 'content':html})
            for i in range(2, int(page_cnt) + 1):
                url = self.__get_url(mechanism_id, i)
                html = self.grab(url)
                self.html_queue.put({'name':'%s_%s' % (mechanism_id, mechanism_name), 'num':i, 'content':html})
            
            self.url_queue.task_done()
    

class DatamineThread(Thread):
    """Parse data from html"""
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def __datamine(self, data):
        '''Get data from html content'''
        soup = BeautifulSoup(data['content'].text, 'html.parser')
        infos = []
        for info in soup.find_all('tr', id=True):
            items = []
            for item in info.find_all('td'):
                items.append(item.get_text())
            infos.append(items)
        return infos
        
    def run(self):
        while True:
            data = self.html_queue.get()
            print('Datamine Thread: get %s_%d' % (data['name'], data['num']))

            store = Storage(data['name'] + '.txt')
            store.save_to_txt(self.__datamine(data))
            self.html_queue.task_done()


class Storage():
    def __init__(self, filename):
        self.path = self.__get_path(filename)

    def __get_path(self, filename):
        path = {
            'Windows': 'D:/litreily/Documents/python/cfachina',
            'Linux': '/mnt/d/litreily/Documents/python/cfachina'
        }.get(platform.system())

        if not os.path.isdir(path):
            os.makedirs(path)
        return '%s/%s' % (path, filename)
    
    def save_to_txt(self, data):
        '''Save data to local file'''
        fid = open(self.path, 'a', encoding='utf-8')

        if not os.path.getsize(self.path):
            fid.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
            ('姓名', '性别', '从业资格号', '投资咨询从业证书号', '任职部门', '职务', '任现职时间'))
        
        for info in data:
            fid.write('\t'.join(info) + '\n')
        fid.close()
    

def main():
    for i in range(1001, 1199):
        url_queue.put(str(i))

    # create and start a spider thread
    st = SpiderThread(url_queue, html_queue)
    st.setDaemon(True)
    st.start()

    # create and start a datamine thread
    dt = DatamineThread(html_queue)
    dt.setDaemon(True)
    dt.start()

    # wait on the queue until everything has been processed
    url_queue.join()
    html_queue.join()


if __name__ == '__main__':
    main()