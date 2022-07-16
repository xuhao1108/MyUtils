#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
import logging
import os
from logging.handlers import RotatingFileHandler

from .my_design_patterns import singleton

__all__ = ['YxhLogger']


@singleton
class YxhLogger(object):
    def __init__(self, formatter=None, stream_handler=True, file_handler=True, path=None, name='log.txt'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.formatter = formatter or logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        if stream_handler:
            self.add_stream_handler()
        if file_handler:
            self.path = os.path.join(path, name) if path else None
            # self.add_file_handler()
            self.add_rotaing_handler()

    def add_stream_handler(self):
        """
        将日志输出到屏幕
        """
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)

        self.logger.addHandler(handler)
        return True

    def add_file_handler(self):
        """
        将日志写入到文件
        """
        if self.path is None:
            return False
        handler = logging.FileHandler(self.path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)

        self.logger.addHandler(handler)
        return True

    def add_rotaing_handler(self):
        """
        日志回滚
        """
        if self.path is None:
            return False
        # 定义一个RotatingFileHandler，最多备份10个日志文件，每个日志文件最大10M
        handler = RotatingFileHandler(self.path, maxBytes=10 * 1024 * 1024, backupCount=10)
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)

        self.logger.addHandler(handler)
        return True

    def get_logger(self):
        return self.logger
