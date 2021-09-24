#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 多线程爬虫
import threading
import time
from threading import Thread, Lock

# from MyUtils import YxhChromeDrver, YxhReadExcel, YxhWriteExcel, read_ini
from . import YxhChromeDrver, YxhReadExcel, YxhWriteExcel, read_ini

# 线程锁
my_lock = Lock()
# 存放线程对象
thread_list = []
# excel写入对象
excel = None
# 存放待爬取的商品链接
goods_url_list = []
# 存放已经爬取过的商品链接
exists_url = []
# 当前爬取到的链接总数
spider_url_num = 0
# 当前爬取总数
spider_data_num = 0


class Page(ChromeDriver):
    def __init__(self):
        # debugger_address_info={'host': '127.0.0.1', 'port': 9222}
        super(Page, self).__init__(headless=True)

    def get_all_goods_url(self, base_url):
        """
        获取商品列表页的所有商品链接
        :param base_url: 商品列表页
        :return:
        """
        # 打开链接
        self.chrome.get(base_url)
        page, max_page = 1, 1
        # 循环抓取商品链接
        while page <= max_page:
            # 打开链接
            # self.chrome.get(base_url + '&page={}'.format(page))
            # 获取所有商品链接
            try:
                a_list = self.get_elements_attribute('', 'href')
            except:
                a_list = []
            global goods_url_list, spider_url_num
            # 去重
            a_list = list(set(a_list).difference(set(exists_url)))
            a_list = list(set(a_list).difference(set(goods_url_list)))
            # 添加到goods_url_list中
            goods_url_list.extend(a_list)
            spider_url_num += len(a_list)
            print('第{}页共获取到{}个链接，目前共获取{}个链接。'.format(page, len(a_list), spider_url_num))
            # 获取最大页码数
            if max_page == 1:
                max_page = self.get_element_text('')
                try:
                    max_page = int(max_page.strip())
                except:
                    max_page = 1
            # 下一页
            try:
                next_btn = self.get_element('')
                # 已经到最后一页了
                if next_btn.get_attribute('disabled'):
                    break
                self.click_element_by_js(next_btn)
            except:
                break
            page += 1

    def run(self):
        pass


class Details(ChromeDriver):
    def __init__(self):
        # debugger_address_info={'host': '127.0.0.1', 'port': 9222}
        super(Details, self).__init__(headless=True)

    def get_goods_info(self, url):
        """
        获取商品信息
        """
        data = []
        # 打开链接
        self.chrome.get(url)
        # ........
        # ........
        # ........
        # ........
        try:
            global excel, spider_data_num
            # 获取锁
            my_lock.acquire()
            # 写入excel
            excel.append_data(data)
            # 已爬取数量+1
            spider_data_num += 1
            # print('第{}次运行，本次需要爬取{}个，目前已爬取{}个，剩余待爬取为{}个。爬取总量为：{}'.format(
            #     spider_index, spider_total, total, spider_total - total, all_total))
            print('共需要爬取{}个，目前已爬取{}个，剩余待爬取为{}个。'.format(
                spider_url_num, spider_data_num, spider_url_num - spider_data_num))
        except:
            pass
        finally:
            # 释放锁
            my_lock.release()

    def run(self):
        while True:
            global goods_url_list
            # 数据为空了
            if len(goods_url_list) == 0:
                break
            try:
                # 获取锁
                my_lock.acquire()
                url = goods_url_list.pop()
            except:
                url = None
            finally:
                # 释放锁
                my_lock.release()
            # 获取商品详细信息
            if url:
                self.get_goods_info(url)


def run():
    pass
