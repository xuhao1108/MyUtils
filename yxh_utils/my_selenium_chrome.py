#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : Selenium下的ChromeDriver
import os
import re
import time
import random
import string
import zipfile

from selenium.webdriver import Chrome, ChromeOptions

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

try:
    # 直接运行本文件时
    from .my_list_dict import delete_key
except:
    # 从外部引用时
    from . import delete_key

__all__ = ['YxhChromeDriver', 'get_random_ua']


class Options(object):
    """
    ChromeOptions
    """

    def __init__(self, binary_location=None, headless=False,
                 no_sandbox=True, max_window=True, window_size=None, fullscreen=False, incognito=False,
                 disable_gpu=True, ignore_errors=True, disable_infobars=True, hide_scroll=True, mute_audio=False,
                 disable_image=False, disable_js=False, disable_java=False,
                 disable_password_alert=True, disable_browser_alert=True, disable_blink_features=True, user_agent=None, debugger_address_info=None,
                 chrome_data_dir=None, proxy_info=None, phone_info=None,
                 lang=None, crx_plugin_list=None):
        """
        初始化浏览器参数
        :param headless: True | False 无头浏览器
        :param no_sandbox: True | False 以最高权限运行
        :param max_window: True | False 是否最大化
        :param window_size: True | False 指定窗口大小
        :param fullscreen: True | False 是否全屏
        :param incognito: True | False 是否无痕
        :param disable_gpu: True | False 是否禁用GPU加速
        :param ignore_errors: True | False 是否忽略证书错误
        :param disable_infobars: True | False 在窗口上不出现‘自动化测试’提示
        :param hide_scroll: True | False 是否不显示滚动条
        :param mute_audio: True | False 是否静音
        :param disable_image: True | False 是否不显示图片
        :param disable_js: True | False 是否禁用js
        :param disable_java: True | False 是否禁用java
        :param disable_password_alert: True | False 禁止弹出密码提示框
        :param disable_browser_alert: True | False 禁止浏览器弹窗
        :param disable_blink_features: True | False 是否隐藏 navigator.webdriver 标志
        :param hide_scroll: True | False 是否隐藏滚动条
        :param user_agent: str 设置请求头
        :param debugger_address_info: dict 监听地址和端口号。参数值样例：{'ip': '127.0.0.1', 'port': 9222}或9222
        :param chrome_data_dir: str  Chrome数据保存路径
        :param proxy_info: dict 代理信息。参数值样例：{'ip': '127.0.0.1', 'port': 9222} {'scheme': 'http','ip': '127.0.0.1', 'port': 9222}
        :param phone_info: dict 页面显示移动端。参数值样例：{'deviceName': 'iPhone 6/7/8'}
        :param lang: str 语言
        :param crx_plugin_list: list 插件列表
        """
        self.proxy_plugin_path = None
        self.options = ChromeOptions()
        # 接管已打开的浏览器
        if debugger_address_info:
            # chrome.exe --remote-debugging-port=9222
            if not isinstance(debugger_address_info, dict):
                debugger_address_info = {'ip': '127.0.0.1', 'port': debugger_address_info}
            self.options.add_experimental_option('debuggerAddress', "{ip}:{port}".format(**debugger_address_info))
        else:
            prefs = {}
            # 指定浏览器位置
            if binary_location:
                self.options.binary_location = binary_location
            # 无头浏览器
            if headless:
                self.options.add_argument('--headless')
            # 以最高权限运行
            if no_sandbox:
                self.options.add_argument('--no-sandbox')
            # 最大化
            if max_window:
                self.options.add_argument('--start-maximized')
            # 指定窗口大小
            if window_size:
                self.options.add_argument('window-size={width}x{height}'.format(**window_size))
            # 浏览器全屏
            if fullscreen:
                self.options.add_argument('--start-fullscreen')
            # 无痕浏览
            if incognito:
                self.options.add_argument('--incognito')
            # 禁用GPU加速
            if disable_gpu:
                self.options.add_argument('--disable-gpu')
            # 忽略证书错误
            if ignore_errors:
                self.options.add_argument('--ignore-certificate-errors')
                self.options.add_argument('--disable-notifications')
                self.options.add_argument('--disable-xss-auditor')
                self.options.add_argument('--disable-web-security')
                self.options.add_argument('--disable-webgl')
                # 在窗口上不出现‘自动化测试’提示
            if disable_infobars:
                # 方法一：可能会无效
                self.options.add_argument('--disable-infobars')
                # 方法二：设置开发者模式启动，该模式下webdriver属性为正常值
                self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
            # 隐藏滚动条, 应对一些特殊页面
            if hide_scroll:
                self.options.add_argument('--hide-scrollbars')
            # 用户数据位置
            if chrome_data_dir:
                # chrome.exe --user-data-dir="......"
                self.options.add_argument(r'--user-data-dir={}'.format(chrome_data_dir))
            # 代理
            self.proxy_info = None
            if proxy_info:
                if isinstance(proxy_info, str):
                    # login:password@socks5://123.123.123.123:3128
                    # login:password@123.123.123.123:3128
                    # socks5://123.123.123.123:3128
                    # 123.123.123.123:3128
                    proxy_item = re.match('(((.*):(.*)@)?((.*)://)?)?(.*):(.*)', proxy_info).groups()
                    proxy_info = {
                        'username': proxy_item[2],
                        'password': proxy_item[3],
                        'scheme': proxy_item[5],
                        'ip': proxy_item[6],
                        'port': proxy_item[7],
                    }
                    # 删除无用的key
                    delete_key(proxy_info)
                self.proxy_info = proxy_info
                self.proxy_info['scheme'] = self.proxy_info.get('scheme', 'http')
                # 认证
                if proxy_info.get('username'):
                    print(self.proxy_info)
                    self.proxy_plugin_path = create_proxy_auth_extension(**self.proxy_info)
                    self.options.add_extension(self.proxy_plugin_path)
                else:
                    # 不认证
                    proxy = '{scheme}://{ip}:{port}'.format(**proxy_info)
                    self.options.add_argument('--proxy-server={}'.format(proxy))
            # 语言
            if lang:
                self.options.add_argument('--lang={}'.format(lang))
            # 添加UA
            if user_agent:
                self.options.add_argument('user-agent="{}"'.format(user_agent))
            # 切换到手机页面
            if phone_info:
                if isinstance(phone_info, str):
                    phone_info = {'deviceName': phone_info}
                self.options.add_experimental_option('mobileEmulation', phone_info)
            # 浏览器静音
            if mute_audio:
                self.options.add_argument("--mute-audio")
            # 不加载图片,提升速度
            if disable_image:
                # 方法一：
                self.options.add_argument('--blink-settings=imagesEnabled=false')
                # 方法二：
                prefs['profile.managed_default_content_settings.images'] = 2
                # prefs = {'profile.managed_default_content_settings.images': 2}
                # self.options.add_experimental_option('prefs', prefs)
            # 禁用JavaScript
            if disable_js:
                self.options.add_argument('--disable-javascript')
            if disable_java:
                self.options.add_argument('--disable-java')
            # 禁止弹出密码提示框
            if disable_password_alert:
                prefs['credentials_enable_service'] = False
                prefs['profile.password_manager_enabled'] = False
                # prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
                # self.options.add_experimental_option('prefs', prefs)
            # 禁用浏览器弹窗
            if disable_browser_alert:
                prefs['profile.default_content_setting_values'] = {'notifications': 2}
                # pref = {'profile.default_content_setting_values': {'notifications': 2}}
                # self.options.add_experimental_option('prefs', pref)
            # 隐藏 navigator.webdriver 标志
            if disable_blink_features:
                # self.options.add_argument('--disable-blink-features')
                self.options.add_argument('--disable-blink-features=AutomationControlled')
            # 添加插件
            if crx_plugin_list:
                if isinstance(crx_plugin_list, str):
                    crx_plugin_list = crx_plugin_list.replace('\r', '').replace('\n', '').split(',')
                for crx_plugin in crx_plugin_list:
                    self.options.add_extension(crx_plugin)
            if prefs:
                self.options.add_experimental_option('prefs', prefs)

    def __del__(self):
        """
        若浏览器未退出，则退出浏览器
        浏览器退出时，若有插件，则删除插件
        :return:
        """
        try:
            if self.proxy_plugin_path:
                os.remove(self.proxy_plugin_path)
        except:
            pass


class Driver(Options):
    """
    ChromeDriver
    """

    def __init__(self, executable_path='chromedriver', implicitly_wait_time=0, cdp=True, mode=By.XPATH, **kwargs):
        """
        初始化浏览器
        :param executable_path: str chromedriver路径
        :param implicitly_wait_time: int 隐式等待时间
        :param mode: str 默认查找元素的方式
        """
        super().__init__(**kwargs)
        self.driver = Chrome(executable_path=executable_path, options=self.options)
        self.driver.implicitly_wait(implicitly_wait_time)
        if cdp:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        # 查找元素的方式
        self.mode = mode

    def add_cookies(self, cookies, refresh=True):
        """
        添加cookies
        :param cookies: cookies列表
        :param refresh: 添加后是否刷新页面
        :return:
        """
        for cookie in cookies:
            [cookie.pop(x) for x in ['sameSite', 'domain', 'expiry', 'expirationDate', ] if x in cookie]
            print(cookie)
            if cookie.get('name', '') != '':
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def get_element(self, pattern, mode=None):
        """
        获取元素，默认xpath
        :param pattern: 查找规则
        :param mode: By.XPATH 查找方式
        :return:
        """
        return self.driver.find_element(mode if mode else self.mode, pattern)

    def get_elements(self, pattern, mode=None):
        """
        获取元素列表
        :param pattern: 查找规则
        :param mode: 查找方式
        :return:
        """
        return self.driver.find_elements(mode if mode else self.mode, pattern)

    def __del__(self):
        """
        若浏览器未退出，则退出浏览器
        :return:
        """
        try:
            self.driver.quit()
        except:
            pass
        super().__del__()


class WaitDriver(Driver):
    """
    WebDriverWait
    """

    def __init__(self, wait_time=30, **kwargs):
        """
        初始化显式等待参数
        :param wait_time: int 显式等待时间
        """
        super().__init__(**kwargs)
        self.wait = WebDriverWait(self.driver, wait_time)

    def wait_element(self, pattern, mode=None):
        """
        获取元素，默认xpath
        :param pattern: 查找规则
        :param mode: By.XPATH 查找方式
        :return:
        """
        return self.wait.until(ec.presence_of_element_located((mode if mode else self.mode, pattern)))

    def wait_elements(self, pattern, mode=None):
        """
        获取元素列表
        :param pattern: 查找规则
        :param mode: 查找方式
        :return:
        """
        return self.wait.until(ec.presence_of_all_elements_located((mode if mode else self.mode, pattern)))

    def switch_to_frame(self, pattern, mode=None, wait_flag=True):
        """
        切换到指定的frame
        :param pattern: 查找规则
        :param mode: By.XPATH 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            self.driver.switch_to.frame(self.wait_element(pattern, mode))
        else:
            self.driver.switch_to.frame(self.get_element(pattern, mode))

    def send_keys_to_element(self, value, pattern, mode=None, clear=True, wait_flag=True):
        """
        往元素里输入文本
        :param value: 输入的文本
        :param pattern: 查找规则
        :param mode: By.XPATH 查找方式
        :param clear: 是否清空原文本
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        if clear:
            element.clear()
        element.send_keys(value)

    def click_element(self, pattern, mode=None, wait_flag=True):
        """
        获取元素列表
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            self.wait_element(pattern, mode).click()
        else:
            self.get_element(pattern, mode).click()

    def select_element(self, pattern, mode=None, index=None, value=None, visible_text=None, wait_flag=True):
        """
        选择下拉框元素的值
        :param pattern: 查找下拉框的规则
        :param mode: 查找下拉框的方式
        :param index: 通过索引定位
        :param value: 通过value值定位
        :param visible_text: 通过文本值定位
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        if index is not None:
            Select(element).select_by_index(index)
        elif value is not None:
            Select(element).select_by_value(value)
        elif visible_text is not None:
            Select(element).select_by_visible_text(visible_text)

    def deselect_element(self, pattern, mode=None, _all=False, index=None, value=None, visible_text=None, wait_flag=True):
        """
        取消选择下拉框元素的值
        :param pattern: 查找下拉框的规则
        :param mode: 查找下拉框的方式
        :param _all: 全部
        :param index: 通过索引定位
        :param value: 通过value值定位
        :param visible_text: 通过文本值定位
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        if _all:
            Select(element).deselect_all()
        elif index is not None:
            Select(element).deselect_by_index(index)
        elif value is not None:
            Select(element).deselect_by_value(value)
        elif visible_text is not None:
            Select(element).deselect_by_visible_text(visible_text)

    def get_element_text(self, pattern, mode=None, wait_flag=True):
        """
        获取元素文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.wait_element(pattern, mode).text
        else:
            return self.get_element(pattern, mode).text

    def get_element_attribute(self, attribute, pattern, mode=None, wait_flag=True):
        """
        获取元素属性
        :param attribute: 元素属性
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.wait_element(pattern, mode).get_attribute(attribute)
        else:
            return self.get_element(pattern, mode).get_attribute(attribute)

    def get_element_property(self, _property, pattern, mode=None, wait_flag=True):
        """
        获取元素属性
        :param _property: 元素属性
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.wait_element(pattern, mode).get_property(_property)
        else:
            return self.get_element(pattern, mode).get_property(_property)

    def get_element_size(self, pattern, mode=None, wait_flag=True):
        """
        获取元素大小
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.wait_element(pattern, mode).size
        else:
            return self.get_element(pattern, mode).size

    def get_element_location(self, pattern, mode=None, wait_flag=True):
        """
        获取元素位置
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.wait_element(pattern, mode).location
        else:
            return self.get_element(pattern, mode).location

    def get_elements_text(self, pattern, mode=None, wait_flag=True):
        """
        获取元素列表的文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return [x.text for x in self.wait_elements(pattern, mode)]
        else:
            return [x.text for x in self.get_elements(pattern, mode)]

    def get_elements_attribute(self, attribute, pattern, mode=None, wait_flag=True):
        """
        获取元素列表属性
        :param attribute: 元素属性
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return [x.get_attribute(attribute) for x in self.wait_elements(pattern, mode)]
        else:
            return [x.get_attribute(attribute) for x in self.get_elements(pattern, mode)]

    def get_elements_property(self, _property, pattern, mode=None, wait_flag=True):
        """
        获取元素列表属性
        :param _property: 元素属性
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return [x.get_property(_property) for x in self.wait_elements(pattern, mode)]
        else:
            return [x.get_property(_property) for x in self.get_elements(pattern, mode)]


class Action(WaitDriver):
    """
    ActionChains
    """

    def get_action(self):
        """
        获取action对象
        :return:
        """
        return ActionChains(self.driver)

    def reset_acitons(self):
        """
        清除动作
        :return:
        """
        ActionChains(self.driver).reset_actions()

    def click_element_by_action(self, pattern=None, mode=None, wait_flag=True, xoffset=0, yoffset=0, reset=True):
        """
        点击元素
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :param xoffset: x轴偏移量
        :param yoffset: y轴偏移量
        :param reset: 是否清除之前的动作
        :return:
        """
        if reset:
            self.reset_acitons()
        if wait_flag:
            ActionChains(self.driver).click(None if pattern is None else self.wait_element(pattern, mode)).move_by_offset(xoffset, yoffset).perform()
        else:
            ActionChains(self.driver).click(None if pattern is None else self.get_element(pattern, mode)).move_by_offset(xoffset, yoffset).perform()

    def click_element_by_action2(self, pattern=None, mode=None, wait_flag=True, xoffset=0, yoffset=0, reset=True):
        """
        点击元素
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :param xoffset: x轴偏移量
        :param yoffset: y轴偏移量
        :param reset: 是否清除之前的动作
        :return:
        """
        if reset:
            self.reset_acitons()
        if wait_flag:
            ActionChains(self.driver).move_to_element_with_offset(self.wait_element(pattern, mode), xoffset, yoffset).click().perform()
        else:
            ActionChains(self.driver).move_to_element_with_offset(self.get_element(pattern, mode), xoffset, yoffset).click().perform()

    def move_to_element_by_action(self, pattern, mode=None, wait_flag=True):
        """
        移动到元素上
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            ActionChains(self.driver).move_to_element(self.wait_element(pattern, mode)).perform()
        else:
            ActionChains(self.driver).move_to_element(self.get_element(pattern, mode)).perform()

    def click_and_hold_element_by_action(self, pattern, mode=None, wait_flag=True, wait_time=0.1):
        """
        按住元素若干秒然后松开
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :param wait_time: 点击元素的停留时间
        :return:
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(wait_time)
        ActionChains(self.driver).release(element).perform()

    def move_element(self, pattern, mode=None, wait_flag=True, xoffset=0, yoffset=0, wait_time=0.5):
        """
        移动元素
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :param xoffset: x轴偏移量
        :param yoffset: y轴偏移量
        :param wait_time: 移动到目标位置后的等待时间
        :return:
        """
        # 点击
        if wait_flag:
            ActionChains(self.driver).click_and_hold(self.wait_element(pattern, mode)).perform()
        else:
            ActionChains(self.driver).click_and_hold(self.get_element(pattern, mode)).perform()
        # 拖动
        ActionChains(self.driver).move_by_offset(xoffset, yoffset).perform()
        time.sleep(wait_time)
        # 松开
        ActionChains(self.driver).release().perform()


class Keys(Action):
    """
    Keys
    """

    @staticmethod
    def get_keys():
        """
        获取Keys对象
        :return:
        """
        return Keys

    def use_copy_key(self):
        self.get_action().key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

    def use_paste_key(self):
        self.get_action().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()


class JS(Keys):
    """
    JS
    """

    def open_window_url(self, url):
        """
        打开标签页
        :param url: 网址
        :return:
        """
        self.driver.execute_script('window.open("{}")'.format(url))

    def close_window_url(self):
        """
        关闭标签页
        :return:
        """
        self.driver.execute_script('window.close()')

    def get_user_agent(self):
        """
        获取浏览器请求头
        """
        return self.driver.execute_script('return navigator.userAgent;')

    def function_element_by_js(self, function_name, pattern, mode=None, wait_flag=True):
        """
        JS调用元素方法
        :param function_name: 方法名
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            self.driver.execute_script('arguments[0].{}();'.format(function_name), self.wait_element(pattern, mode))
        else:
            self.driver.execute_script('arguments[0].{}();'.format(function_name), self.get_element(pattern, mode))

    def click_element_by_js(self, pattern, mode=None, wait_flag=True):
        """
        点击元素
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        self.function_element_by_js('click', pattern, mode, wait_flag)

    def scroll_to_element_by_js(self, pattern, mode=None, wait_flag=True):
        """
        滑动到元素的位置
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        self.function_element_by_js('scrollIntoView', pattern, mode, wait_flag)

    def scroll_to(self, height=10000):
        """
        滚动到指定位置
        :param height: 指定高度
        :return:
        """
        self.driver.execute_script('document.documentElement.scrollTop={}'.format(height))

    def scroll_to_top(self, offset=0):
        """
        滚动到页面顶部
        :param offset: 偏移量
        :return:
        """
        self.scroll_to(height=0 + offset)

    def scroll_to_body_bottom(self, offset=0):
        """
        滚动到页面底部
        :param offset: 偏移量
        :return:
        """
        self.driver.execute_script('var offset = {};window.scrollTo(0, document.body.scrollHeight + offset)'.format(offset))

    def scroll_to_bottm_by_step(self, step=None, offset=0):
        """
        滑动到页面底部
        :param step: 步长
        :param offset: 偏移量
        :return:
        """
        start = 0

        client_height = self.driver.execute_script('return document.body.clientHeight;')
        scroll_height = self.driver.execute_script('return document.body.scrollHeight;')
        stop = max(client_height, scroll_height)

        # 分辨率作为每次滑动的步长
        if step is None:
            step = self.driver.execute_script('return window.screen.height;')
        elif isinstance(step, float):
            step = int((stop - start) * step)
        # 依次滑动
        while stop - start > 0:
            self.scroll_to(start)
            time.sleep(0.1)
            start += step
        # 滑动到末尾
        self.scroll_to(start)

        # 动态加载的
        retry_num = 0
        while retry_num < 3:
            # 若动态加载的，则获取新高度，并重新滑动
            client_height = self.driver.execute_script('return document.body.clientHeight;')
            scroll_height = self.driver.execute_script('return document.body.scrollHeight;')
            stop = max(client_height, scroll_height)
            # 到底了
            if stop <= start:
                return True

            # 依次滑动
            while stop - start > 0:
                self.scroll_to(start)
                time.sleep(0.1)
                start += step
            # 滑动到末尾
            self.scroll_to(start)
            retry_num += 1

    def get_element_inner_text_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素文本；从起始位置到终止位置的内容，但不包含Html标签。
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].innerText;', self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].innerText;', self.get_element(pattern, mode))

    def get_element_inner_html_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素HTML；从起始位置到终止位置的内容，包含Html标签。
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].innerHTML;', self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].innerHTML;', self.get_element(pattern, mode))

    def get_element_outer_text_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素文本；
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].outerText;', self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].outerText;', self.get_element(pattern, mode))

    def get_element_outer_html_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素HTML；除了包含innerHTML的全部内容外, 还包含对象标签本身。
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].outerHTML;', self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].outerHTML;', self.get_element(pattern, mode))

    def get_element_size_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素大小
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        return {
            'width': self.driver.execute_script('arguments[0].offsetWidth;', element),
            'height': self.driver.execute_script('arguments[0].offsetHeight;', element)
        }

    def get_element_location_by_js(self, pattern, mode=None, wait_flag=True):
        """
        获取元素位置
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        get_left_js = """
            function getOffsetLeft(obj) {
                var tmp = obj.offsetLeft;
                var val = obj.offsetParent;
                while (val != null) {
                    tmp += val.offsetLeft;
                    val = val.offsetParent;
                }
                return tmp;
            }
            return getOffsetLeft(arguments[0]);
        """
        get_top_js = """
            function getOffsetTop(obj) {
                var tmp = obj.offsetTop;
                var val = obj.offsetParent;
                while (val != null) {
                    tmp += val.offsetTop;
                    val = val.offsetParent;
                }
                return tmp;
            }
            return getOffsetTop(arguments[0]);
        """
        if wait_flag:
            element = self.wait_element(pattern, mode)
        else:
            element = self.get_element(pattern, mode)
        return {
            'x': self.driver.execute_script(get_left_js, element),
            'y': self.driver.execute_script(get_top_js, element)
        }

    def set_element_inner_text_by_js(self, text, pattern, mode=None, wait_flag=True):
        """
        获取元素文本；从起始位置到终止位置的内容，但不包含Html标签。
        :param text: 元素文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].innerText = "{}" ;'.format(text), self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].innerText = "{}" ;'.format(text), self.get_element(pattern, mode))

    def set_element_inner_html_by_js(self, html, pattern, mode=None, wait_flag=True):
        """
        获取元素HTML；从起始位置到终止位置的内容，包含Html标签。
        :param html: 元素标签和文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].innerHTML = "{}";'.format(html), self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].innerHTML = "{}";'.format(html), self.get_element(pattern, mode))

    def set_element_outer_text_by_js(self, text, pattern, mode=None, wait_flag=True):
        """
        获取元素文本；
        :param text: 元素文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].outerText = "{}" ;'.format(text), self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].outerText = "{}" ;'.format(text), self.get_element(pattern, mode))

    def set_element_outer_html_by_js(self, html, pattern, mode=None, wait_flag=True):
        """
        获取元素HTML；除了包含innerHTML的全部内容外, 还包含对象标签本身。
        :param html: 元素标签和文本
        :param pattern: 查找规则
        :param mode: 查找方式
        :param wait_flag: 是否等待元素出现
        :return:
        """
        if wait_flag:
            return self.driver.execute_script('arguments[0].outerHTML = "{}";'.format(html), self.wait_element(pattern, mode))
        else:
            return self.driver.execute_script('arguments[0].outerHTML = "{}";'.format(html), self.get_element(pattern, mode))


class Captcha(JS):
    """
    Captcha
    """

    @staticmethod
    def get_track(distance, current=0, v=0, t=0.2, add_a=2, reduce_a=-3, mid=None):
        """
        获取在一定路程内，每个时间段内移动的距离
        :param distance: 总路程
        :param current: 当前位置
        :param v: 初速度
        :param t: 时间间隔
        :param add_a: 加速度
        :param reduce_a: 减速度
        :param mid: 加减速的标志点
        :return: 每个时间段内移动的距离
        """
        track = []
        mid = mid if mid else distance * 4 / 5
        while current < distance:
            if current < mid:
                a = add_a
            else:
                a = reduce_a
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def move_slider(self, element, distance, offset_list=None, wait_time=0.5, current=0, v=0, t=0.2, add_a=2, reduce_a=-3, mid=None):
        """
        滑动元素，一定的距离
        :param element: 滑动的元素
        :param distance: 总路程
        :param offset_list: [5, -5] 移动到指定位置后的偏移量
        :param wait_time:  移动到指定位置后的等待时间
        :param current:  初始位置
        :param add_a: 加速度
        :param reduce_a: 减速度
        :param t: 时间间隔
        :param v: 初速度
        :param mid: 加减速的标志点
        :return:
        """
        offset_list = offset_list if offset_list else [5, -5]
        # 点击“滑块”
        ActionChains(self.driver).click_and_hold(element).perform()
        # 拖动“滑块”
        for x in self.get_track(distance, current, v, t, add_a, reduce_a, mid):
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        # 偏移量
        for x in offset_list:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(wait_time)
        # 松开“滑块”
        ActionChains(self.driver).release().perform()

    # TODO 谷歌验证码 hcaptcha
    def get_google_site_key(self):
        """
        获取谷歌验证码密钥
        """
        return self.get_element_attribute('data-sitekey', '//div[@class="g-recaptcha"]')

    def set_google_site_key(self, response):
        """
        设置谷歌验证码结果密钥
        :param response: 结果密钥
        """
        try:
            g_captcha_response = self.get_element('//textarea[@name="g-captcha-response"]')
            self.driver.execute_script('arguments[0].innerHTML = "{}"'.format(response), g_captcha_response)
        except:
            pass

    def get_hcaptcha_site_key(self):
        """
        获取hcaptcha验证码密钥
        """
        return self.get_element_attribute('sitekey', '//h-captcha')

    def set_hcaptcha_site_key(self, response):
        """
        设置hcaptcha验证码结果密钥
        将令牌放入h-captcha-response和g-recaptcha-response隐藏元素中，然后提交表单。
        请注意，hcaptcha还有一个回调。如果没有要提交的表单，您必须浏览网站代码并找到回调。
        :param response: 结果密钥
        """
        try:
            # 写入结果
            # iframe的data-hcaptcha-response
            iframe = self.get_element('//h-captcha/iframe')
            self.driver.execute_script('arguments[0].setAttribute("data-hcaptcha-response", "{}");'.format(response), iframe)
            # textarea的输入框
            self.driver.execute_script('$("h-captcha > textarea").val("{}")'.format(response))
            # 调用回调函数
            self.driver.execute_script('hcaptcha.getRespKey = function (t) {return "";}')
            self.driver.execute_script('hcaptcha.getResponse = function (t) {return "' + response + '";}')
            self.driver.execute_script('document.querySelector("#new_user > div > div:nth-child(4) > h-captcha").onVerify();')
            # self.driver.execute_script('document.querySelector("#new_user > div > div:nth-child(4) > h-captcha").onVerify("{}");'.format(response))
        except:
            pass
        try:
            g_captcha_response = self.get_element('//textarea[@name="g-captcha-response"]')
            self.driver.execute_script('arguments[0].innerHTML = "{}"'.format(response), g_captcha_response)
        except:
            pass


class YxhChromeDriver(Captcha):
    """
    YxhChromeDriver
    """

    @staticmethod
    def get_position(size, location):
        """
        获取元素四个顶点的位置
        :param size: 元素大小
        :param location: 元素位置
        :return:
        """
        return {
            'left': location['x'],
            'top': location['y'],
            'right': location['x'] + size['width'],
            'bottom': location['y'] + size['height'],
        }


def create_proxy_auth_extension(ip, port, username, password, scheme='http', plugin_path=None):
    """
    创建代理认证插件
    :param ip: ip
    :param port:
    :param username:
    :param password:
    :param scheme:
    :param plugin_path: 插件保存路径
    :return:
    """
    if plugin_path is None:
        plugin_path = r'{}-{}-{}.zip'.format(scheme, ip, port)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Dobel Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=ip,
        port=port,
        username=username,
        password=password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def get_random_ua():
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        # 收集
        # "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    ]
    return random.choice(user_agent)


if __name__ == '__main__':
    pass
