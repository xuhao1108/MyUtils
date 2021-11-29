#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
from yxh_utils import *

obj = YxhChromeDriver()


# mdc_1129 > develop > xxx.tar.gz
def get_file_list():
    item_class_list = obj.get_elements_attribute('class', 'xpath_pattern')
    result = []
    for index, item_class in enumerate(item_class_list):
        # 文件夹
        if 'clss-dir' in item_class:
            # 点击文件夹
            obj.click_element_by_js('xpath_pattern/div[{}]'.format(index))
            # 获取文件列表
            get_file_list()
            # 返回上一层
            obj.click_element_by_js('xpath_pattern2222/div[{}]'.format(index))
        # 文件
        elif 'class-file' in item_class:
            result.append(obj.get_element_text('xpath_pattern2222/div[{}]'.format(index)))