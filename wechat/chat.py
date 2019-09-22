#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import random
import time
import json
import config
import os
import io
from pyqrcode import QRCode
import logging as log


class Chat():
    '''parise someone who you truly love'''

    def __init__(self, user, showTitle=True):
        self._showTitle = showTitle
        self._user = user
        self._times = 10
        self._interval = 1

        log.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',
                        level=log.INFO)

        # itchat.auto_login(enableCmdQR=2)
        # self.user = itchat.search_friends(username)[0]

    @property
    def times(self):
        return self._times

    @times.setter
    def times(self, value):
        self._times = value

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    def load_data(self, datafile):
        if not os.path.isfile(datafile):
            log.info('Not Found file ' + datafile)
            return

        with open(datafile, 'r', encoding='utf-8') as f:
            datas = json.loads(f.read(), encoding='utf-8')

        if self._showTitle:
            self.titles = datas['title']
            self.tones = datas['tone']
            self.seps = datas['separator']
        self.contents = datas['content']

    @classmethod
    def get_QR(self, uuid, enableCmdQR=False, picDir=None):
        picDir = picDir or config.DEFAULT_QR
        qrStorage = io.BytesIO()
        qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
        qrCode.png(qrStorage, scale=10)
        with open(picDir, 'wb') as f:
            f.write(qrStorage.getvalue())
        return qrStorage

    @classmethod
    def open_QR(self):
        for get_count in range(10):
            log.info('Getting uuid of QR code')
            uuid = itchat.get_QRuuid()
            while uuid is None:
                uuid = itchat.get_QRuuid()
                time.sleep(1)
            log.info('Getting QR Code')
            if self.get_QR(uuid):
                break
            elif get_count >= 9:
                log.error('Failed to get QR Code, please restart the program')
                sys.exit()
        log.info('Please scan the QR Code to login')
        return uuid

    @classmethod
    def login(self, uuid):
        '''Login wechat for send message'''
        # uuid = self.open_QR()
        waitForConfirm = False

        while 1:
            status = itchat.check_login(uuid)
            if status == '200':
                break
            elif status == '201':
                if waitForConfirm:
                    log.info('Please press confirm')
                    waitForConfirm = True
            elif status == '408':
                log.info('Reloading QR Code')
                waitForConfirm = False

        userInfo = itchat.web_init()
        itchat.show_mobile_login()
        log.info('Start get contacts, this may take sometime')
        itchat.get_friends(True)
        log.info('Login successfully as %s' % userInfo['User']['NickName'])
        itchat.start_receiving()

    def _build_msg(self, random_index):
        """build messages from json file"""
        title = ''
        tone = ''
        sep = ''
        if self._showTitle:
            title = self.titles[random.randint(0, len(self.titles)) - 1]

        if title:
            tone = self.tones[random.randint(0, len(self.tones)) - 1]
            sep = self.seps[random.randint(0, len(self.seps)) - 1]

        content = self.contents[random_index]

        return '{}{}{}{}'.format(title, tone, sep, content)

    def _send_msg(self):
        random_list = random.sample(range(0, len(self.contents)-1), self._times)
        user = itchat.search_friends(name=self._user)[0]
        for i in random_list:
            user.send(self._build_msg(i))
            time.sleep(1)

    def run(self):
        random.seed(time.time())
        self._send_msg()


if __name__ == '__main__':
    log.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',
                    level=log.INFO)

    praise = Chat(u'增增')
    praise.load_data('msg.json')
    praise.login()
    praise.run()
