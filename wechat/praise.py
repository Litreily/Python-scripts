#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import random
import time
import json

class Praise:
    """parise someone who you truly love"""
    def __init__(self, username, datafile, times=10, showTitle=True):
        with open(datafile, 'r') as f:
            datas = json.loads(f.read())

        self.showTitle = showTitle

        if self.showTitle:
            self.titles = datas['title']
            self.tones = datas['tone']
            self.seps = datas['separator']
        self.contents = datas['content']

        self.times = times

        itchat.auto_login(enableCmdQR=2)
        self.user = itchat.search_friends(username)[0]

    def _build_msg(self, random_index):
        """build messages from json file"""
        title = ''
        tone = ''
        sep = ''
        if self.showTitle:
            title = self.titles[random.randint(0, len(self.titles)) - 1]

        if title:
            tone = self.tones[random.randint(0, len(self.tones)) - 1]
            sep = self.seps[random.randint(0, len(self.seps)) - 1]

        content = self.contents[random_index]

        return '{}{}{}{}'.format(title, tone, sep, content)

    def _send_msg(self):
        random_list = random.sample(range(0, len(self.contents)-1), self.times)
        for i in random_list:
            self.user.send(self._build_msg(i))
            time.sleep(1)

    def run(self):
        random.seed(time.time())
        self._send_msg()


if __name__ == '__main__':
    praise = Praise('增增', 'msg.json', 10)
    praise.run()
