#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 打码平台
import os
import time
import json
import base64
import requests
from hashlib import md5

from io import BytesIO
from PIL import Image

__all__ = ['YxhChaoJiYing', 'YxhLianZhong', 'YxhTuJian', 'YxhTwoCaptcha', 'YxhAntiCaptcha']


class YxhChaoJiYing(object):
    def __init__(self, username, password):
        """
        初始化数据
        :param username: 用户账号
        :param password: 用户密码
        """
        # 用户的账号密码
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        # 开发者的软件id
        self.soft_id = 'fde46b182a3c58d5f02970eb4c16a937'
        # 请求头
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        # 请求结果
        self.result = None

    def get_result(self, image_path, type_id, len_min=0):
        """
        识别图形验证码，价格：https://www.chaojiying.com/price.html
        :param image_path: 图片本地路径或图片URL路径
        :param type_id: 图片类型
        :param len_min: 图片类型
        :return: str
        """
        try:
            url = 'https://upload.chaojiying.net/Upload/Processing.php'
            data = {
                'user': self.username,
                'pass2': self.password,
                'softid': self.soft_id,
                'codetype': type_id,
                'len_min': len_min,
                'file_base64': get_image_base64(image_path)
            }
            # # 图片文件二进制流(或是称之为内存流,文件流,字节流的概念)
            # files = {
            #     'userfile': ('a.jpg', image_path)
            # }
            # result = json.loads(requests.post(url, data=data, files=files, headers=self.headers).text)
            result = json.loads(requests.post(url, data=data, headers=self.headers).text)
            self.result = result
            if result['err_no'] == 0:
                return result['pic_str']
            else:
                print('请求失败了，原因：{}'.format(result))
                return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''

    def post_error(self):
        """
        图形验证码识别错误
        :return: bool
        """
        try:
            url = 'https://upload.chaojiying.net/Upload/ReportError.php'
            data = {
                'user': self.username,
                'pass2': self.password,
                'softid': self.soft_id,
                'id': self.result['pic_id'],
            }
            result = json.loads(requests.post(url, json=data, headers=self.headers).text)
            if result['err_no'] == 0:
                return True
            else:
                print('请求失败了，原因：{}'.format(result))
                return False
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return False

    def get_score(self):
        """
        获取用户剩余点数
        :return: dict
        """
        try:
            url = 'https://upload.chaojiying.net/Upload/GetScore.php'
            data = {
                'user': self.username,
                'pass2': self.password
            }
            result = json.loads(requests.post(url, json=data, headers=self.headers).text)
            if result['err_no'] == 0:
                return result
            else:
                print('请求失败了，原因：{}'.format(result))
                return result
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return {}


class YxhLianZhong(object):
    def __init__(self, username, password):
        """
        初始化数据
        :param username: 用户账号
        :param password: 用户密码
        """
        # 用户的账号密码
        self.username = username
        self.password = password
        # 开发者的软件id和secret
        self.soft_id = 26925
        self.secret = 'cydv0bamxkt0tUQCCN8pucM4agbZ3cKc0FqomfJo'
        # 请求头
        self.headers = {
            'Host': 'v2-api.jsdama.com',
            'Connection': 'keep-alive',
            'Content-Length': '298',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
            'Content-Type': 'text/json'
        }
        # 请求结果
        self.result = None

    def get_result(self, image_path, type_id, min_len=0, max_len=0, worker_tips_id=0):
        """
        识别图形验证码，价格：https://www.jsdati.com/docs/price
        :param image_path: 图片本地路径或图片URL路径
        :param type_id: 图片类型
        :param min_len: 识别时需输⼊的最⼩⻓度
        :param max_len: 识别时需输⼊的最大⻓度
        :param worker_tips_id: ⼈⼯提示模板ID
        :return: str
        """
        try:
            url = 'https://v2-api.jsdama.com/upload'
            data = {
                'softwareId': self.soft_id,
                'softwareSecret': self.secret,
                'username': self.username,
                'password': self.password,
                'captchaData': get_image_base64(image_path),
                'captchaType': type_id,
                'captchaMinLength': min_len,
                'captchaMaxLength': max_len,
                'workerTipsId': worker_tips_id
            }
            result = json.loads(requests.post(url, json=data, headers=self.headers).text)
            self.result = result
            if result['code'] == 0:
                return result['data']['recognition']
            else:
                print('请求失败了，原因：{}'.format(result))
                return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''

    def post_error(self):
        """
        图形验证码识别错误
        :return: bool
        """
        try:
            url = 'https://v2-api.jsdama.com/report-error'
            data = {
                'softwareId': self.soft_id,
                'softwareSecret': self.secret,
                'username': self.username,
                'password': self.password,
                'captchaId': self.result['data']['captchaId']
            }
            result = json.loads(requests.post(url, json=data, headers=self.headers).text)
            if result['code'] == 0:
                return True
            else:
                print('请求失败了，原因：{}'.format(result))
                return False
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return False

    def get_score(self):
        """
        获取用户剩余点数
        :return: dict
        """
        try:
            url = 'https://v2-api.jsdama.com/check-points'
            data = {
                'softwareId': self.soft_id,
                'softwareSecret': self.secret,
                'username': self.username,
                'password': self.password
            }
            result = json.loads(requests.post(url, json=data, headers=self.headers).text)
            if result['code'] == 0:
                return result['data']
            else:
                print('请求失败了，原因：{}'.format(result))
                return result
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return {}


class YxhTuJian(object):
    def __init__(self, username, password):
        """
        初始化数据
        :param username: 用户账号
        :param password: 用户密码
        """
        # 用户的账号密码
        self.username = username
        self.password = password
        # 开发者的软件id
        self.softid = 'cce56384732d4aada9121d9cb1bb9dee'
        # 请求结果
        self.result = None

    def get_result(self, image_path, type_id=3, angle=None, type_name=None, remark=None, image_back_path=None, content=None, title_image=None):
        """
        识别图形验证码，价格：https://www.ttshitu.com/price.html?spm=null
        :param image_path: 图片本地路径或图片URL路径
        :param type_id: 图片类型
        :param angle: 旋转角度：当typeid为14时旋转角度 默认90
        :param type_name: 无感学习子类型名称(可为空)：用户自定义（需自己记住,不同时为不同的无感学习）。typeid为(7: 无感学习)时传
        :param remark: 备注字段 如：填写计算结果 (兼容unicode) 遇到中文乱码情况 请unicode编码以免造成错误。
        :param image_back_path: 缺口识别2张图传背景图需要
        :param content: 快速点选需要，标题内容 如：填写 "你好"中文请unicode编码以免造成错误。
        :param title_image: 快速点选需要，标题内容 如：填写 "你好"中文请unicode编码以免造成错误。
        :return: str
        """
        try:
            url = 'https://api.ttshitu.com/predict'
            data = {
                'username': self.username,
                'password': self.password,
                'typeid': type_id,
                'image': get_image_base64(image_path),
                'softid': self.softid
            }
            if angle is not None:
                data['angle'] = angle
            if type_name is not None:
                data['typename'] = type_name
            if remark is not None:
                data['remark'] = remark
            if image_back_path is not None:
                data['imageback'] = get_image_base64(image_back_path)
            if content is not None:
                data['content'] = content
            if title_image is not None:
                data['title_image'] = title_image
            print(data)
            result = json.loads(requests.post(url, json=data).text)
            self.result = result
            if result['success']:
                return result['data']['result']
            else:
                print('请求失败了，原因：{}'.format(result))
                return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''

    def get_error(self):
        """
        图形验证码识别错误
        :return: bool
        """
        try:
            url = 'https://api.ttshitu.com/reporterror.json'
            data = {
                'id': self.result['data']['id'],
            }
            result = json.loads(requests.post(url, json=data).text)
            if result['success']:
                return True
            else:
                print('请求失败了，原因：{}'.format(result))
                return False
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return False

    def get_score(self):
        """
        获取用户剩余点数
        :return: dict
        """
        try:
            url = 'https://api.ttshitu.com/queryAccountInfo.json'
            data = {
                'username': self.username,
                'password': self.password
            }
            result = json.loads(requests.get(url, json=data).text)
            if result['success']:
                return result['data']
            else:
                print('请求失败了，原因：{}'.format(result))
                return result
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return {}


class YxhTwoCaptcha(object):
    def __init__(self, api_key):
        """
        初始化数据。推荐注册链接：https://2captcha.com?from=12602328
        :param api_key: 用户密钥
        """
        self.api_key = api_key
        self.soft_id = 3209
        # 请求结果
        self.task_id = ''

    def get_in(self, data):
        """
        谷歌验证码第一步，获取任务id
        :param data: 请求数据
        :return:
        """
        url = 'https://2captcha.com/in.php'
        response = requests.post(url, data=data).json()
        if response['status'] == 1:
            # 报错时会用到task_id
            self.task_id = response['request']
            return self.task_id
        else:
            print('任务创建失败，原因：{}'.format(response))
            return ''

    def get_res(self, action, callback_url=None):
        """
        谷歌验证码第二步，获取验证结果
        :param action: 获取动作
        :param callback_url: 回调url
        :return:
        """
        try:
            url = 'https://2captcha.com/res.php'
            data = {
                'key': self.api_key,
                'action': action,
                'id': self.task_id,
                'json': 1,
            }
            if callback_url:
                data['addr'] = callback_url
            result = requests.get(url, params=data).json()
            if result['status'] == 1:
                return result['request']
            else:
                # print('任务尚未完成...')
                return ''
        except Exception as e:
            print('结果获取失败，原因：{}'.format(e))
            return ''

    def get_error(self):
        """
        图形验证码识别错误
        :return:
        """
        return self.get_res('reportbad', self.result['request'])

    def add_pingback(self, addr):
        """
        添加回调地址
        :param addr: 回调地址
        :return:
        """
        return self.get_res('add_pingback', callback_url=addr)

    def get_pingback(self, addr):
        """
        查看回调地址
        :param addr: 回调地址
        :return:
        """
        return self.get_res('get_pingback', callback_url=addr)

    def del_pingback(self, addr):
        """
        删除回调地址
        :param addr: 回调地址
        :return:
        """
        return self.get_res('del_pingback', callback_url=addr)

    def get_google_result(self, url, site_key, invisible=0):
        """
        识别谷歌图形验证码，
        :param url: 网页网址
        :param site_key: 谷歌密钥
        :param invisible: 1：reCAPTCHA不可见；0：可见。
        :return:
        """
        try:
            # 第一步：获取任务ID
            data = {
                'key': self.api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': url,
                'invisible': invisible,
                'json': 1,
                'soft_id': self.soft_id
            }
            self.get_in(data)
            if self.task_id == '':
                return ''
            # 第二步：获取结果
            for i in range(0, 120, 5):
                print('等待获取请求中......')
                time.sleep(5)
                result = self.get_res('get')
                if result != '':
                    return result
            return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''

    def get_hcaptcha_result(self, url, site_key, invisible=0, _data=None, user_agent=None, pingback_url=None, proxy=None, proxy_type=None):
        """
        识别hcaptcha
        :param url: 网页网址
        :param site_key: hcaptcha密钥
        :param invisible: 1：reCAPTCHA不可见；0：可见。默认值为0
        :param _data: hcaotcha请求参数
        :param user_agent: hcaotcha请求头
        :param pingback_url: 回调地址
        :param proxy: 代理信息 user:password@ip:port
        :param proxy_type: 代理类型
        :return:
        """
        try:
            # 第一步：获取任务ID
            data = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'sitekey': site_key,
                'pageurl': url,
                'invisible': invisible,
                'json': 1,
                'soft_id': self.soft_id
            }
            if _data:
                data['data'] = _data
            if user_agent:
                data['userAgent'] = user_agent
            if proxy:
                data['proxy'] = proxy
            if proxy_type:
                data['proxytype'] = proxy_type
            # 判断是否有回调
            if pingback_url is not None:
                data['pingback'] = pingback_url
                # 添加到回调地址中
                self.add_pingback(pingback_url)
            # 获取任务ID
            self.get_in(data)
            # 回调不返回信息
            if pingback_url is None and self.task_id == '':
                return ''
            # 第二步：获取结果
            for i in range(0, 120, 5):
                print('等待获取请求中......')
                time.sleep(5)
                result = self.get_res('get')
                if result != '':
                    return result
            return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''


class YxhAntiCaptcha(object):
    def __init__(self, client_key):
        """
        初始化数据。推荐注册链接：http://getcaptchasolution.com/3qwjnfj0k9
        :param client_key: 用户密钥
        """
        self.client_key = client_key
        self.soft_id = 988
        # 请求结果
        self.task_id = 0

    def create_task(self, task, language_pool='en', callback_url=None):
        """
        创建任务
        :param task: 任务对象
        :param language_pool: 用于设置备用工作人员语言。仅适用于图片人机验证。目前有以下备用语言可用：en（默认设置）：英语队列。rn：多个国家：俄罗斯、乌克兰、白俄罗斯、哈萨克斯坦
        :param callback_url: 自愿使用的网址，我们将向其发送人机验证任务处理结果。会通过 AJAX POST 请求发送内容，内容类似于 getTaskResult 方法的内容。
        :return:
        """
        url = 'https://api.anti-captcha.com/createTask'
        data = {
            'clientKey': self.client_key,
            'task': task,
            'softId': self.soft_id,
            'languagePool': language_pool,
        }
        headers = {
            'Content-type': 'application-json'
        }
        if callback_url:
            data['callbackUrl'] = callback_url
        response = requests.post(url, json=data, headers=headers).json()
        if response['errorId'] == 0:
            # 报错时会用到task_id
            self.task_id = response['taskId']
            return self.task_id
        else:
            print('任务创建失败，原因：{}；{}'.format(response['errorCode'], response['errorDescription']))
            return 0

    def get_task_result(self):
        """
        获取任务执行结果
        :return:
        """
        url = 'https://api.anti-captcha.com/getTaskResult'
        data = {
            'clientKey': self.client_key,
            'taskId': self.task_id
        }
        headers = {
            'Content-type': 'application-json'
        }
        response = requests.post(url, json=data, headers=headers).json()
        if response['errorId'] == 0:
            if response['status'] == 'processing':
                # print('任务尚未完成...')
                return ''
            elif response['status'] == 'ready':
                return response['solution']
        else:
            print('结果获取失败，原因：{}；{}'.format(response['errorCode'], response['errorDescription']))
            return ''

    def get_hcaptcha_result(self, url, site_key, proxy=None):
        """
        识别hcaptcha，推荐链接：https://2captcha.com?from=12602328
        :param url: 网页网址
        :param site_key: hcaptcha密钥
        :param proxy: 代理信息 {'user_gent':'浏览器请求头', 'scheme':'代理ip类型', 'ip':'地址', 'port':'端口', 'username':'用户名', 'password':'密码'}
        :return:
        """
        try:
            # 第一步：创建任务
            task = {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': url,
                'websiteKey': site_key,
            }
            if proxy:
                # 修改类型为有代理的
                task['type'] = 'HCaptchaTask'
                # 浏览器请求头
                task['userAgent'] = proxy['user_gent']
                # 代理ip
                task['proxyType'] = proxy['scheme']
                task['proxyAddress'] = proxy['ip']
                task['proxyPort'] = proxy['port']
                # 代理ip认证信息
                if proxy.get('username'):
                    task['proxyLogin'] = proxy['username']
                if proxy.get('password'):
                    task['proxyPassword'] = proxy['password']
            self.create_task(task)
            if self.task_id == 0:
                return ''
            # 第二步：获取结果
            for i in range(0, 120, 5):
                print('等待获取请求中......')
                time.sleep(5)
                result = self.get_task_result()
                if result != '':
                    return result['gRecaptchaResponse']
            return ''
        except Exception as e:
            print('出错了，原因：{}'.format(e))
            return ''


def get_image_base64(image_path):
    """
    将图片转为base64
    :param image_path: 图片本地路径或图片URL路径
    :return:
    """
    # 从本地读取图片
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data.decode()
    # 从url读取图片
    else:
        response = requests.get(image_path)
        base64_data = base64.b64encode(BytesIO(response.content).read())
        return base64_data.decode()


if __name__ == '__main__':
    pass
