#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 数组和字典的扩展应用

__all__ = ['sort_list_dict', 'sort_dict', 'list_to_dict', 'delete_key']


def sort_list_dict(data, values=None, reverse=True):
    """
    将字典数组按照字典里的指定字段进行排序
    :param data: 字典树组
    :param values: 排序字段
    :param reverse: True：降序，False：升序
    :return:
    """
    if isinstance(values, str):
        values = [values]
    return sorted(data, key=lambda e: tuple([e.__getitem__(value) for value in values]), reverse=reverse)


def sort_dict(data, key=True, values=None, reverse=True):
    """

    :param data:
    :param key:
    :param values:
    :param reverse:
    :return:
    """


def list_to_dict(keys, values):
    """
    将两个数组转为字段
    :param keys: keys数组
    :param values: values数组
    :return:
    """
    return dict(zip(keys, values))


def delete_key(data, option=None):
    """
    当value为指定值时，则删除key
    :param data: 字典对象
    :param option: 当value为指定值时，则删除key
    :return: 
    """
    delete_keys = [k for k, v in data.items() if v == option]
    for key in delete_keys:
        data.pop(key)


if __name__ == '__main__':
    pass
