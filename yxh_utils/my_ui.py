#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
from tkinter import *
from tkinter.messagebox import *

from .my_91sfy import Yxh91ShenFanYun
from .my_config import read_ini, write_ini

__all__ = ['LoginFrame']


class LoginFrame(object):
    def __init__(self, title, token, project_name, success_func, ini_path='config.ini', width=400, height=150, *args, **kwargs):
        """
        初始化登录界面
        :param master: 根界面
        """
        self.token = token
        self.project_name = project_name
        self.success_func = success_func
        self.ini_path = ini_path

        self.args = args
        self.kwargs = kwargs

        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        # 设置窗口大小，在屏幕的居中位置
        self.root.geometry('%dx%d+%d+%d' % (width, height, (self.root.winfo_screenwidth() - width) / 2, (self.root.winfo_screenheight() - height) / 2))
        # 注册页面
        self.login_frame = None
        # 注册码变量
        self.register_code = StringVar(value=self.get_register_code_from_ini())
        # 初始化本地页面
        self.init_login_frame()

        self.root.mainloop()

    def init_login_frame(self):
        """
        初始化登录界面
        :return:
        """
        # 创建Frame
        self.login_frame = Frame(self.root)
        self.login_frame.pack()
        # 创建控件
        Label(self.login_frame).grid(row=0, stick=W)

        Label(self.login_frame, text='注册码: ').grid(row=1, stick=W, pady=10)
        Entry(self.login_frame, textvariable=self.register_code).grid(row=1, column=1, stick=E)

        Button(self.login_frame, text='登陆', command=self.login_event).grid(row=3, stick=W, pady=10)
        Button(self.login_frame, text='退出', command=self.login_frame.quit).grid(row=3, column=1, stick=E)

    def login_event(self):
        """
        登录按钮点击事件
        :return:
        """
        try:
            obj = Yxh91ShenFanYun(self.token, self.project_name, register_code=self.register_code.get())
            result = obj.login()
            showinfo('提示', '登录成功！' if result is True else result)
            if result is True:
                self.set_register_code_to_ini()
                self.root.destroy()

                self.success_func(*self.args, **self.kwargs)
                return True
            return False
        except Exception as e:
            showerror(title='出错了！', message='{}！'.format(e))
            return False

    def get_register_code_from_ini(self):
        try:
            config = read_ini(self.ini_path)
            return config['register_code']
        except:
            return None

    def set_register_code_to_ini(self):
        try:
            write_ini({'register_code': self.register_code.get()}, self.ini_path)
        except:
            pass
