#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
import os
import random
import time
import win32clipboard

from datetime import date
from datetime import timedelta
from PIL import Image, ImageGrab
from io import BytesIO

__all__ = ['gennerator_card_id', 'get_time_str', 'set_clipboard_image', 'get_clipboard_image']

codelist = [
    {'code': '110000', 'district': '北京市'}, {'code': '110101', 'district': '东城区'}, {'code': '110102', 'district': '西城区'}, {'code': '110105', 'district': '朝阳区'},
    {'code': '110106', 'district': '丰台区'}, {'code': '110107', 'district': '石景山区'}, {'code': '110108', 'district': '海淀区'}, {'code': '110109', 'district': '门头沟区'},
    {'code': '110111', 'district': '房山区'}, {'code': '110112', 'district': '通州区'}, {'code': '110113', 'district': '顺义区'}, {'code': '110114', 'district': '昌平区'},
    {'code': '110115', 'district': '大兴区'}, {'code': '110116', 'district': '怀柔区'}, {'code': '110117', 'district': '平谷区'}, {'code': '110118', 'district': '密云区'},
    {'code': '110119', 'district': '延庆区'}, {'code': '120000', 'district': '天津市'}, {'code': '120101', 'district': '和平区'}, {'code': '120102', 'district': '河东区'},
    {'code': '120103', 'district': '河西区'}, {'code': '120104', 'district': '南开区'}, {'code': '120105', 'district': '河北区'}, {'code': '120106', 'district': '红桥区'},
    {'code': '120110', 'district': '东丽区'}, {'code': '120111', 'district': '西青区'}, {'code': '120112', 'district': '津南区'}, {'code': '120113', 'district': '北辰区'},
    {'code': '120114', 'district': '武清区'}, {'code': '120115', 'district': '宝坻区'}, {'code': '120116', 'district': '滨海新区'}, {'code': '120117', 'district': '宁河区'},
    {'code': '120118', 'district': '静海区'}, {'code': '120119', 'district': '蓟州区'}, {'code': '130000', 'district': '河北省'}, {'code': '130100', 'district': '石家庄市'},
    {'code': '130102', 'district': '长安区'}, {'code': '130104', 'district': '桥西区'}, {'code': '130105', 'district': '新华区'}, {'code': '130107', 'district': '井陉矿区'},
    {'code': '130108', 'district': '裕华区'}, {'code': '130109', 'district': '藁城区'}, {'code': '130110', 'district': '鹿泉区'}, {'code': '130111', 'district': '栾城区'},
    {'code': '130121', 'district': '井陉县'}, {'code': '130123', 'district': '正定县'}, {'code': '130125', 'district': '行唐县'}, {'code': '130126', 'district': '灵寿县'},
    {'code': '130127', 'district': '高邑县'}, {'code': '130128', 'district': '深泽县'}, {'code': '130129', 'district': '赞皇县'}, {'code': '130130', 'district': '无极县'},
    {'code': '130131', 'district': '平山县'}, {'code': '130132', 'district': '元氏县'}, {'code': '130133', 'district': '赵县'}, {'code': '130181', 'district': '辛集市'},
    {'code': '130183', 'district': '晋州市'}, {'code': '130184', 'district': '新乐市'}, {'code': '130200', 'district': '唐山市'}, {'code': '130202', 'district': '路南区'},
    {'code': '130203', 'district': '路北区'}, {'code': '130204', 'district': '古冶区'}
]


def gennerator_card_id():
    """
    随机生成身份证号
    :return:
    """
    age = random.randint(1, 99)
    # 地区码
    district_id = random.choice(codelist)['code']
    # 年
    year = date.today().year - age
    # 月日
    month_day = (date.today() + timedelta(days=random.randint(1, 366))).strftime('%m%d')
    # 顺序码
    random_number = random.randint(100, 300)
    # 前十七位
    card_id = f'{district_id}{year}{month_day}{random_number}'

    count = 0
    # 权重项
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码映射
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'}
    for index in range(0, len(card_id)):
        count += int(card_id[index]) * weight[index]
    card_id = card_id + checkcode[str(count % 11)]
    return card_id


def get_time_str(time_stamp):
    """
    根据时间戳获取字符串
    :param time_stamp:
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))


def get_google_authenticator_code(secret):
    """
    获取谷歌认证码
    """
    secret = secret.strip().replace(' ', '')
    if len(secret) % 8 != 0:
        secret += '=' * (8 - len(secret) % 8)
    msg = struct.pack(">Q", int(time.time()) // 30)
    key = base64.b32decode(secret, True)
    h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
    o = h[19] & 15
    h = str((struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000)
    return h.rjust(6, '0')


def set_clipboard_image(image_path):
    """
    将图片复制到剪贴板
    :param image_path: 图片路径
    :return:
    """
    # 此时模式为RGB
    image = Image.open(image_path)
    output = BytesIO()
    image.save(output, 'BMP')
    # BMP图片有14字节的header，需要额外去除
    data = output.getvalue()[14:]
    output.close()

    # 复制到剪贴板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def get_clipboard_image(image_path):
    """
    将剪贴板图片保存到本地
    :param image_path: 图片保存路径
    :return:
    """
    im = ImageGrab.grabclipboard()
    im.save(image_path)


if __name__ == '__main__':
    pass
