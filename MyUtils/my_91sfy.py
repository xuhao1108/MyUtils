#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 91神烦云
import requests

try:
    # 直接运行本文件时
    from .my_computer import generate_driver_id
except:
    # 从外部引用时
    from . import generate_driver_id

__all__ = ['Yxh91ShenFanYun']

get_flag_list = [
    '试用', '试用时间',
    '注册码登录', '查询注册码时间', '客户端解绑注册码',
    '检查更新', '获取项目键名称值'
]
post_flag_list = [
    # 注册码管理
    '查询所有注册码', '解绑注册码', '冻结注册码', '解冻注册码', '删除注册码',
    '新建注册码', '续费注册码', '修改注册码项目名称', '修改注册码备注信息', '获取注册码使用情况', '获取条件数据总数', '上一页', '下一页',
    # 项目名称管理
    '获取项目名称列表', '添加项目名称', '删除项目名称', '修改项目名称', '修改项目版本号', '修改项目公告', '修改更新文件', '修改更新状态',
    # 其他相关通信
    '查询操作日志', '获取日志数据总数', '上一页日志', '下一页日志',
    # 项目自定义键值的相关通信
    '查询项目键值', '添加项目键值', '修改项目值', '删除项目键值', '获取项目键值数据总数', '上一页键值', '下一页键值',
    # 处理web管理端数据
    'web用户登陆', 'web用户退出', 'web注册码查询', 'web解绑', 'web冻结', 'web修改项目名称', 'web修改备注', 'web清理过期注册码',
    'web导出注册码', 'web项目管理查询', 'web项目删除', 'web项目查询2', 'web项目查询1', 'web项目创建', 'web项目修改',
    'web用户管理查询', 'web用户创建', 'web用户信息', 'web用户删除', 'web用户修改'
]


class Yxh91ShenFanYun(object):
    def __init__(self, token, project_name, driver_id=None, register_code=None):
        """
        初始化
        http://bbs.91shenfan.com/forum.php?mod=viewthread&tid=1011&highlight=%E6%96%87%E6%A1%A3
        :param token: 百宝云软件token
        :param project_name: 百宝云软件项目名称
        :param driver_id: 本机机器码
        :param register_code: 注册码
        """
        self.token = token
        self.project_name = project_name
        self.driver_id = driver_id if driver_id else generate_driver_id()
        self.register_code = register_code
        # 访问令牌
        self.access_token = None

    def get_url(self, data):
        """
        获取get接口链接
        :param data: 参数
        :return: 
        """
        url = 'https://get.91shenfan.com/api/{}'.format(self.token)
        return requests.get(url, data=data).text

    def post_url(self, data):
        """
        获取post接口链接
        :param data: 参数
        :return: 
        """
        url = 'https://post.91shenfan.com/api/{}'.format(self.token)
        return requests.post(url, data=data).text

    @staticmethod
    def get_error_message(response):
        """
        获取错误信息
        :param response:
        :return:
        """
        try:
            return response.split(':')[-1].replace('.', '')
        except:
            return response

    def login(self, register_code=None):
        """
        注册码登录
        :param register_code: 注册码
        :return:
        """
        data = {
            'flag': '注册码登录',
            '项目名称': self.project_name,
            '注册码': register_code or self.register_code,
            '机器码': self.driver_id,
        }
        response = self.post_url(data)
        # 登录成功|34|11886554&yanxuhao
        # 注册码已经冻结
        # 注册码已经过期
        # 注册码已经绑定其他机器
        # 注册码不正确
        if '登录成功' in response:
            self.access_token = response.split('|')[-1].split('&')[0]
            return True
        else:
            return self.get_error_message(response)

    def unbind(self, password=None, register_code=None):
        """
        客户端解绑注册码
        :param password: 解绑密码
        :param register_code: 注册码
        :return:
        """
        data = {
            'flag': '客户端解绑注册码',
            '项目名称': self.project_name,
            '注册码': register_code or self.register_code,
            '机器码': self.driver_id,
            # '解绑密码': '此参数可以为空,只能本地解绑,无法异地解绑'
        }
        if password is not None:
            data['解绑密码'] = password
        response = self.post_url(data)
        # 注册码与机器码不对应
        if '1' in response:
            return True
        else:
            return self.get_error_message(response)

    def logout(self, register_code=None):
        """
        注册码登出
        :param register_code: 注册码
        :return:
        """
        data = {
            'flag': '注册码退出',
            '注册码': register_code or self.register_code,
            '访问令牌': self.access_token
        }
        response = self.post_url(data)
        # 只有当前客户端,才能退出注册码
        # 注册码已经退出
        # 操作成功
        if '操作成功' in response:
            return True
        else:
            return self.get_error_message(response)

    def offline(self, register_code=None):
        """
        注册码下线
        :param register_code: 注册码
        :return:
        """
        data = {
            'flag': '注册码下线',
            '注册码': register_code or self.register_code,
            '机器码': self.driver_id,
        }
        response = self.post_url(data)
        # 只有当前客户端,才能退出注册码
        # 注册码已经退出
        # 操作成功
        if '操作成功' in response:
            return True
        else:
            return self.get_error_message(response)

    def get_status(self, register_code=None):
        """
        查询注册码时间
        :param register_code: 注册码
        :return: 分钟
        """
        data = {
            'flag': '查询注册码时间',
            '项目名称': self.project_name,
            '注册码': register_code or self.register_code,
            '机器码': self.driver_id,
            '访问令牌': self.access_token,
        }
        response = self.post_url(data)
        # 注册码已经下线
        # 注册码只能在一个客户端使用
        # 注册码已过期
        if '注册码已经下线' in response:
            return True
        else:
            return self.get_error_message(response)


if __name__ == '__main__':
    pass
