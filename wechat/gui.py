# -*- coding: utf-8 -*-

import tkinter as tk
from config import PX, PY, LIST_INFO, DEFAULT_QR
from functools import partial
from PIL import Image, ImageTk
from abc import ABCMeta, abstractmethod


class GUI(tk.Tk, metaclass=ABCMeta):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(800, 480))

    def create_widgets(self):
        self.title('Happy sister')
        self.f_login = tk.LabelFrame(
            self, text='账号登录', width=200, height=280, padx=PX, pady=PY)
        self.f_datalist = tk.LabelFrame(
            self, text='数据信息', width=600, height=280, padx=PX, pady=PY)
        self.f_control = tk.LabelFrame(
            self, text='消息控制', width=800, height=180, padx=PX, pady=PY)

        self.f_login.grid(row=0, column=0)
        self.f_datalist.grid(row=0, column=1)
        self.f_control.grid(row=1, column=0, columnspan=2)

        self.f_login.grid_propagate(0)
        self.f_datalist.grid_propagate(0)
        self.f_control.grid_propagate(0)

        self.create_f_login()
        self.create_f_datalist()
        self.create_f_control()
        self.create_f_statusbar()

    def create_f_login(self):
        '''create frame for login'''
        self.btn_refresh = tk.Button(self.f_login,
                                     text="刷新登录二维码",
                                     relief=tk.GROOVE,
                                     command=self.refresh_handler)
        self.btn_refresh.grid(row=0, column=0, columnspan=2,
                              padx=4, ipadx=8, sticky='WE')

        # label which use to show QR code
        self.lbl_QA = tk.Label(self.f_login, relief=tk.SUNKEN)

        self.lbl_QA.grid(row=1, column=0, columnspan=2, padx=4, pady=PY)

        tk.Label(self.f_login, text='当前发送对象:', anchor=tk.W).grid(
            row=2, column=0, padx=4, pady=PY, sticky=tk.W)
        self.lbl_receiver = tk.Label(self.f_login, text='emily',
                                     width=10, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_receiver.grid(row=2, column=1, padx=4, pady=PY, sticky='WE')

    def create_f_datalist(self):
        '''create frame for datalist'''
        self.lsbs = list()
        self.btns = list()
        # listbox of love
        for key, i in zip(LIST_INFO, range(len(LIST_INFO))):
            tk.Label(self.f_datalist, text=key).grid(
                row=0, column=i*2, columnspan=2,
                padx=PX, ipady=PY, sticky=tk.W)

            listval = tk.StringVar(value=LIST_INFO[key]['info'])

            lsbox = tk.Listbox(self.f_datalist,
                               height=10,
                               listvariable=listval,
                               exportselection=0,
                               selectmode='browse')
            lsbox.grid(row=1, column=i*2, columnspan=2, padx=PX)
            lsbox.select_set(0)
            self.lsbs.append(lsbox)

            btn_info = LIST_INFO[key]['btn']
            for btn_name, j in zip(btn_info, range(len(btn_info))):
                handler = partial(self.list_handler, i, j)
                self.btns.append(tk.Button(
                    self.f_datalist,
                    text=btn_name,
                    relief=tk.GROOVE,
                    command=handler))
                self.btns[-1].grid(row=2, column=i*2+j, padx=PX, pady=PY,
                                   ipadx=8, sticky='we')

    def create_f_control(self):
        '''create frame for message control'''
        self.btn_rand = tk.Button(self.f_control, text='随机', relief=tk.GROOVE)
        self.btn_rand.grid(
            row=0, column=0, padx=PX, pady=PY, ipadx=16, sticky=tk.W)

        self.entry_msg = tk.Entry(self.f_control, width=92)
        self.entry_msg.grid(row=0, column=1, padx=PX, sticky='we')

        self.btn_send = tk.Button(self.f_control, text='发送', relief=tk.GROOVE)
        self.btn_send.grid(
            row=0, column=2, padx=PX, pady=PY, ipadx=16, sticky=tk.W)

        tk.Label(self.f_control, text='发送次数', anchor=tk.W).grid(
            row=1, column=0, padx=PX, pady=PY, sticky=tk.W)
        self.entry_times = tk.Entry(self.f_control, width=8)
        self.entry_times.grid(row=2, column=0, sticky=tk.W, padx=4)

        tk.Label(self.f_control, text='间隔时间(s)', anchor=tk.W).grid(
            row=3, column=0, padx=PX, pady=PY, sticky=tk.W)
        self.entry_interval = tk.Entry(self.f_control, width=8)
        self.entry_interval.grid(row=4, column=0, sticky=tk.W, padx=4)

        self.text_log = tk.Text(
            self.f_control, wrap='word', width=92, height=8)
        self.text_log.grid(row=1, column=1, rowspan=4, sticky='we')

        self.btn_start = tk.Button(self.f_control, text='开始', relief=tk.GROOVE)
        self.btn_start.grid(row=1, column=2, rowspan=4, padx=PX, sticky='nswe')

    def create_f_statusbar(self):
        self.statusbar = tk.Label(self, text='please login first.',
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky='WE')

    def status(self, message):
        self.statusbar['text'] = message

    def list_handler(self, lsb_index, btn_index):
        try:
            btn_text = self.btns[lsb_index*2 + btn_index].config('text')[-1]
            sel_lsb = self.lsbs[lsb_index]
            sel_index = sel_lsb.curselection()[0]
        except IndexError as ie:
            self.status(ie.__str__())
            return

        if btn_text == '选择':
            self.lbl_receiver['text'] = sel_lsb.get(sel_index)
        elif btn_text == '移除':
            sel_lsb.delete(sel_index)
        elif btn_text == '收藏':
            if sel_lsb.get(sel_index) not in self.lsbs[0].get(0, tk.END):
                self.lsbs[0].insert(tk.END, sel_lsb.get(sel_index))

    def refresh_QR(self, imgfile='QR.png'):
        image = Image.open(imgfile)
        out = image.resize((180, 180), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(out)
        self.lbl_QA.configure(image=self.img)

    @abstractmethod
    def refresh_handler(self):
        pass

    @abstractmethod
    def on_closing(self):
        pass
