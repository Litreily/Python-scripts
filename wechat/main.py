# -*- coding: utf-8 -*-

import itchat
from gui import GUI
from chat import Chat
import logging as log
import time
from threading import Thread


class WechatApp(GUI):
    def __init__(self):
        GUI.__init__(self)

        self.create_widgets()
        self.refresh_QR(imgfile='blank.png')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def refresh_handler(self):
        self.refresh_QR()
        pass

    def on_closing(self):
        self.destroy()
        itchat.logout()


def login_wechat():
    chat = Chat(u'增增')
    uuid = chat.open_QR()
    chat.login(uuid)


def main():
    t1 = Thread(target=login_wechat)
    t1.start()

    app = WechatApp()
    app.mainloop()
    pass

if __name__ == "__main__":
    main()
