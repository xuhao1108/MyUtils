#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ini文件的读写
import os
import configparser

from .my_design_patterns import singleton

__all__ = ['read_ini', 'write_ini', 'YxhConfig']


def read_ini(ini_path='config.ini', encoding=None, user_header_key=False):
    """
    读取配置文件
    :param ini_path: 配置文件路径
    :param encoding: 配置文件编码格式
    :param user_header_key: 是否将配置文件的表头作为一级key
    :return:
    """
    config = {}
    # 读取配置文件
    cp = configparser.ConfigParser()
    if encoding:
        cp.read(ini_path, encoding=encoding)
    else:
        for encoding in ['utf-8', 'utf_8_sig', 'gbk']:
            try:
                cp.read(ini_path, encoding=encoding)
                break
            except:
                pass
    # 按照键值对形式保存
    for header in cp.sections():
        if user_header_key and header not in config:
            config[header] = {}
        for key, value in cp.items(header):
            value = value.strip()
            # 数值类
            if 'num' in key or 'time' in key:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except:
                    pass
            elif 'list' in key:
                value = value.split(',')
            # 路径类
            elif 'path' in key or 'dir' in key:
                try:
                    value = os.path.realpath(value)
                except:
                    pass
            if user_header_key:
                config[header][key] = value
            else:
                config[key] = value
    return config


def write_ini(data_dict, ini_path='config.ini', encoding=None, section='config'):
    cp = configparser.ConfigParser()
    if encoding:
        cp.read(ini_path, encoding=encoding)
    else:
        for encoding in ['utf-8', 'utf_8_sig', 'gbk']:
            try:
                cp.read(ini_path, encoding=encoding)
                break
            except:
                pass
    if section not in cp.sections():
        cp.add_section(section)

    for key, value in data_dict.items():
        cp.set(str(section), str(key), str(value))
    cp.write(open(ini_path, 'w'))


@singleton
class YxhConfig(object):

    def __init__(self, path):

        config = read_ini(path)
        if config.get('label') is None:
            config['label'] = 'ALL'
        elif config.get('label') != 'ALL':
            config['label'] = [x.split(',') for x in config['label'].split(';')]

        self.config = config
        self.__dict__.update(config)
