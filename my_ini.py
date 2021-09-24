#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ini文件的读写
import os
import configparser


def read_ini(ini_path, encoding='utf-8', user_header_key=False):
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
    cp.read(ini_path, encoding=encoding)
    # 按照键值对形式保存
    for header in cp.sections():
        if user_header_key and header not in config:
            config[header] = {}
        for key, value in cp.items(header):
            value = value.strip()
            # 数值类
            if 'num' in key:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except:
                    pass
            # 路径类
            elif 'path' in key or 'dir' in key:
                try:
                    base_path = os.path.split(ini_path)[0]
                    value = os.path.join(base_path, value)
                except:
                    pass
            if user_header_key:
                config[header][key] = value
            else:
                config[key] = value
    return config
