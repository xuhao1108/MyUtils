#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 模拟登录邮箱
import json
import os
import re
import time
from PIL import Image

from .my_selenium_chrome import YxhChromeDriver
from .my_captcha import YxhLianZhong

__all__ = ['Yxh163Email', 'YxhGoogleEmail']


class BaseEmail(object):
    def __init__(self, username, password, captcha_username=None, captcha_password=None):
        """
        初始化
        :param username: 邮箱用户名
        :param password: 邮箱密码
        :param captcha_username: 打码平台用户名
        :param captcha_password: 打码平台密码
        """
        self.username = username
        self.password = password

        self.captcha_username = captcha_username
        self.captcha_password = captcha_password

        self.all_email_list = []
        self.read_email_list = []
        self.unread_email_list = []

        self.chrome = YxhChromeDriver()

    def login(self):
        """
        登录
        """
        pass

    def get_all_email(self, page=1):
        """
        获取所有邮件
        """
        pass

    def get_read_email(self):
        """
        获取已读邮件
        """
        pass

    def get_unread_email(self):
        """
        获取未读邮件
        """
        pass


class Yxh163Email(BaseEmail):
    def login(self):
        """
        登录
        """
        # 打开登录页面
        self.chrome.driver.get('https://mail.163.com/')
        # 切换到登录的iframe
        iframe_location = self.chrome.get_element_location_by_js('//div[@id="loginDiv"]/iframe')
        self.chrome.switch_to_frame('//div[@id="loginDiv"]/iframe')
        # 输入账号密码
        self.chrome.send_keys_to_element(self.username, '//input[@class="j-inputtext dlemail j-nameforslide"]')
        self.chrome.send_keys_to_element(self.password, '//input[@class="j-inputtext dlpwd"]')
        # 点击登录
        self.chrome.click_element_by_js('//*[@id="dologin"]')
        # 处理验证码
        retry_num = 0
        while retry_num < 3:
            if self.slove_captcha(iframe_location):
                break
            else:
                retry_num += 1
        # 点击登录
        self.chrome.click_element_by_js('//*[@id="dologin"]')
        time.sleep(3)
        # 点击“收信”按钮
        if self.chrome.get_element('//li[@class="js-component-component ra0 nb0"]'):
            self.chrome.click_element_by_js('//li[@class="js-component-component ra0 nb0"]')
            return True
        else:
            return False

    def slove_captcha(self, iframe_location):
        """
        处理验证码
        :param iframe_location: 登录面板的位置
        :return:
        """
        # 移动到并点击“点此进行验证”
        self.chrome.click_element_by_action('//div[@class="yidun_tips"]')
        time.sleep(3)
        # 获取验证码图片
        # img_url = self.chrome.get_element_attribute('src', '//div[@class="yidun_bgimg"]/img[1]')
        # 获取要点击的文字
        # click_string = self.chrome.get_element_text('//div[@class="yidun_tips__answer"]/span')
        # click_string = click_string.strip().replace('"', '').replace(' ', ',')
        image_path = self.get_captcha_image(iframe_location)
        # 获取打码结果
        captcha_obj = YxhLianZhong(self.captcha_username, self.captcha_password)
        # 获取3个坐标点
        result = captcha_obj.get_result(image_path, 1303)
        click_position_list = [x.split(',') for x in result.split('|')]
        try:
            os.remove(image_path)
        except:
            pass
        # 图片url大小为：480*240
        # 网页图片大小为：340*170
        # 计算原坐标点
        # proportion = 340 / 480
        proportion = 480 / 480
        click_position_list = [(int(x[0]) * proportion, int(x[1]) * proportion) for x in click_position_list]
        # 显示验证码图片
        # self.chrome.driver.execute_script('document.querySelector("div.yidun_panel").style.display = "block";')
        # location = self.chrome.get_element_location('//div[@class="yidun_bgimg"]/img[1]')
        # print(location)
        # 依次点击文字
        input('start?:')
        for click_position in click_position_list:
            # 起始点为“点此进行验证”，y轴需要先往上偏移 图片的高度
            self.chrome.driver.execute_script('document.querySelector("div.yidun_panel").style.display = "block";')
            code_location = self.chrome.get_element_location_by_js('//div[@class="yidun_bgimg"]/img[1]')
            self.chrome.click_element_by_action2('//div[@class="yidun_bgimg"]/img[1]', xoffset=click_position[0], yoffset=click_position[1])
            time.sleep(1)
        time.sleep(3)
        input('ok?:')
        # 获取验证结果
        result_text = self.chrome.get_element_text('//div[@class="yidun_tips"]/span[2]')
        if result_text == '验证成功':
            return True
        else:
            return False

    def get_captcha_image(self, iframe_location):
        """
        获取验证码截图
        :param iframe_location: 父面板位置
        :return:
        """
        captcha_path = 'captcha.png'
        # 显示图片
        self.chrome.driver.execute_script('document.querySelector("div.yidun_panel").style.display = "block";')
        # 保存屏幕截图
        self.chrome.driver.save_screenshot(captcha_path)
        # 获取图片位置
        code_location = self.chrome.get_element_location_by_js('//div[@class="yidun_bgimg"]/img[1]')
        # 获取图片和按钮的大小
        code_size = self.chrome.get_element_size('//div[@class="yidun_bgimg"]/img[1]')
        div_size = self.chrome.get_element_size('//div[@class="yidun_tips"]')
        crop_info = (
            iframe_location['x'] + code_location['x'],
            iframe_location['y'] + code_location['y'],
            iframe_location['x'] + code_location['x'] + code_size['width'],
            iframe_location['y'] + code_location['y'] + code_size['height'] + div_size['height']
        )
        image = Image.open(captcha_path)
        image = image.crop(crop_info)
        image.save(captcha_path)
        return captcha_path


class YxhGoogleEmail(BaseEmail):
    pass


if __name__ == '__main__':
    pass
