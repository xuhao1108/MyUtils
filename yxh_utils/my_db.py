#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
import pymysql

from .my_design_patterns import singleton

__all__ = ['YxhDB']


@singleton
class YxhDB(object):
    def __init__(self, db, host=None, port=None, username=None, password=None, charset=None):
        self.db = pymysql.connect(host=host or 'localhost', port=port or 3306,
                                  user=username or 'root', password=password or 'root',
                                  db=db, charset=charset or 'utf8')


if __name__ == '__main__':
    main()
