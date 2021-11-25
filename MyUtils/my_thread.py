#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 获取多线程返回值
from threading import Thread

__all__ = ['YxhThread']


class YxhThread(Thread):
    def __init__(self, *args, **kwargs):
        """
        能够获取线程返回值
        :param target: 线程函数
        :param args: 函数参数列表
        :param args: 函数参数字典
        :param name: 线程名称
        """
        super(YxhThread, self).__init__(*args, **kwargs)
        self.result = None

    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def get_result(self):
        """
        获取线程返回值
        :return:
        """
        try:
            return self.result
        except Exception:
            return None


if __name__ == '__main__':
    pass
