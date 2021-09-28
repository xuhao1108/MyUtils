#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/11 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 邮件
import os
import re
import time
import poplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header, decode_header
from email.utils import formataddr, parseaddr
from email.parser import Parser


class YxhSendEmail(object):
    def __init__(self, host, sender, password, port=0, ssl=True, sender_name=None):
        """
        初始化参数
        :param host: 邮箱的host
        :param sender: 发送者邮箱
        :param port: 邮箱的port，默认值：普通：25，ssl：465
        :param ssl: 是否使用ssl加密
        :param password: 发送者邮箱密码
        """
        # 邮件发送者
        self.sender = sender
        # 邮件发送者昵称
        self.sender_name = sender_name
        # 连接邮箱并登录
        if ssl:
            self.smtp = smtplib.SMTP_SSL(host, port or 465)
        else:
            self.smtp = smtplib.SMTP(host, port or 25)
        self.smtp.login(self.sender, password)

    def get_email_list(self):
        pass

    def send_email(self, subject, body, receiver, receiver_name=None, message_type='plain', message_encoding='utf-8', atts=None):
        """
        发送邮件
        :param subject:  主题
        :param body: 正文
        :param receiver: str | list 收件人邮箱
        :param receiver_name: str | list 收件人昵称
        :param message_type: 类型
        :param message_encoding: 编码格式
        :param atts: str | list 附件路径
        :return:
        """
        try:
            message = MIMEMultipart()
            # 邮件主题，编码
            message['Subject'] = Header(subject, message_encoding)
            if self.sender_name:
                # 发件人昵称、发件人邮箱
                message['From'] = formataddr([self.sender_name, self.sender])
            else:
                # 发件人邮箱，编码
                message['From'] = Header(self.sender, message_encoding)

            if isinstance(receiver, list):
                receiver = ','.join(receiver)
            if receiver_name:
                # 收件人昵称、收件人邮箱
                message['To'] = formataddr([receiver_name, receiver])
            else:
                message['To'] = Header(receiver, message_encoding)
            receiver = receiver.split(',')

            # 邮件正文，格式，编码
            content = MIMEText(body, message_type, message_encoding)
            message.attach(content)
            # 若有附件,则创建带附件的邮件
            if atts:
                atts = atts if isinstance(atts, list) else [atts]
                # 依次吧附件添加到邮件对象中
                for att in atts:
                    message.attach(create_att(att))
            # 发件人，收件人，邮件内容
            self.smtp.sendmail(self.sender, receiver, message.as_string())
            print('邮件发送成功,收件人:{}'.format(receiver))
            return True
        except Exception as e:
            print('邮件发送失败,收件人:{},原因:{}'.format(receiver, e))
            return False

    def __del__(self):
        try:
            # 退出邮箱登录
            self.smtp.quit()
        except:
            pass


def create_att(file_path, file_name=None):
    """
    创建文件附件
    :param file_path: 文件完整路径
    :param file_name: 文件名
    :return: 文件附件对象
    """
    att = MIMEApplication(open(file_path, 'rb').read())
    if file_name is None:
        file_name = os.path.basename(file_path)
    att.add_header('Content-Disposition', 'attachment', filename=file_name)
    return att


class YxhReadEmail(object):
    def __init__(self, host, username, password, port=0, ssl=True):
        """
        连接到POP3邮箱服务器
        :param host: 服务器地址
        :param username: 用户名
        :param password: 密码
        :param port: 邮箱的port，默认值：普通：110，ssl：995
        :param ssl 是否使用ssl加密
        """
        # 连接到POP3服务器
        if ssl:
            self.server = poplib.POP3_SSL(host, port or 995)
        else:
            self.server = poplib.POP3(host, port or 110)
        # 身份认证
        self.server.user(username)
        self.server.pass_(password)

    def get_email_len(self):
        """
        获取邮箱列表长度
        :return:
        """
        resp, mails, octets = self.server.list()
        return len(mails)

    def get_all_email_info(self):
        """
        获取所有邮件信息
        :return:
        """
        email_info_list = []
        for index in range(self.get_email_len(), 0, -1):
            # 索引号从1开始
            email_info = self.get_email_info(index)
            email_info_list.append(email_info)
        return email_info_list

    def get_email_info(self, index):
        """
        获取指定下标的邮件信息
        :param index: 邮件下标，索引从1开始
        :return:
        """
        resp, lines, octets = self.server.retr(index)
        # lines存储了邮件的原始文本的每一行
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 解析邮件
        msg = Parser().parsestr(msg_content)
        # 获取邮件时间,格式化收件时间
        date_time = time.strptime(msg.get('Date')[0:24], '%a, %d %b %Y %H:%M:%S')
        time_stamp = int(time.mktime(date_time))
        # 邮件时间格式转换
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', date_time)
        email_info = {'time_str': date_time, 'time_stamp': time_stamp}
        get_format_info(msg, email_info)
        return email_info

    def download_email_attr(self, index, save_path):
        """
        下载邮件的附件
        :param index: 邮件下标，索引从1开始
        :param save_path: 邮件保存路径
        :return:
        """
        email_info = self.get_email_info(index)
        for attr in email_info['attr']:
            try:
                with open(os.path.join(save_path, attr['filename']), 'wb') as f:
                    f.write(attr['content'])
            except Exception as e:
                print('文件保存失败，原因：{}'.format(e))

    def delete_email(self, index):
        """
        删除邮件
        :param index: 邮件下标，索引从1开始
        :return:
        """
        self.server.dele(index)

    def __del__(self):
        try:
            # 关闭连接
            self.server.quit()
        except:
            pass


def get_format_info(msg, data, indent=0):
    """
    获取邮件内容格式化信息
    :param msg: 格式化前的邮件文本
    :param data: 保存格式化后的数据
    :param indent: 缩进标志
    :return:
    """
    if not data.get('text'):
        data['text'] = ''
    if not data.get('html'):
        data['html'] = ''
    if not data.get('attachment'):
        data['attachment'] = []
    # indent用于缩进显示
    if indent == 0:
        for header in ['From', 'To', 'Subject', 'Cc']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                    data[header.lower()] = value
                elif header == 'From':
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = {'name': name, 'address': addr}
                    data[header.lower()] = value
                else:
                    # 接收人，抄送人可能是多个
                    for item in value.split(','):
                        hdr, addr = parseaddr(item)
                        name = decode_str(hdr)
                        item = {'name': name, 'address': addr}
                        if not data.get(header.lower()):
                            data[header.lower()] = []
                        data[header.lower()].append(item)
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            get_format_info(part, data, indent + 1)
    else:
        content_type = msg.get_content_type()
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        # content = content.decode(charset)
        if not charset:
            return 1
        if content_type == 'text/plain':
            content = content.decode(charset)
            data['text'] += content.replace('\r\n \r\n', '\n')
        elif content_type == 'text/html':
            content = content.decode(charset)
            data['html'] += content.replace('<meta http-equiv="Content-Type" content="text/html; charset=GB18030">', '').replace('\n', '')
        elif content_type == 'application/octet-stream':
            # print(charset)
            try:
                dh = decode_header(msg.get_filename())
                file_name = dh[0][0].decode(dh[0][1])
            except:
                file_name = 'default.txt'
            data['attachment'].append({'filename': file_name, 'content': content})


def decode_str(s):
    """
    字符编码转换
    :param s:
    :return:
    """
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    """
    获得msg的编码
    :param msg:
    :return:
    """
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_service_info():
    """
    各大平台的邮箱服务器信息
    :return:
    """
    default_smtp_port = 25
    default_imap_port = 143
    default_pop_port = 110

    default_ssl_smtp_port = 1
    default_ssl_imap_port = 1
    default_ssl_pop_port = 1
    return {
        'qq': {
            'smtp': {'host': 'smtp.qq.com', 'port': 25, 'ssl_port': [465, 587]},
            'imap': {'host': 'smtp.qq.com', 'port': 0, 'ssl_port': [465, 587]},
            'pop3': {'host': 'pop.qq.com', 'port': 0, 'ssl_port': 995}
        },
        'wx_work': {
            'smtp': {'host': 'smtp.exmail.qq.com', 'port': 0, 'ssl_port': 465},
            'imap': {'host': 'imap.exmail.qq.com', 'port': 0, 'ssl_port': 993},
            'pop3': {'host': 'pop.exmail.qq.com', 'port': 0, 'ssl_port': 995}
        },
        'outlook': {
            'smtp': {'host': 'smtp-mail.outlook.com', 'port': 0, 'ssl_port': 587},
            'imap': {'host': 'outlook.office365.com', 'port': 0, 'ssl_port': 993},
            'pop3': {'host': 'outlook.office365.com', 'port': 0, 'ssl_port': 995}
        },
        '163': {
            'smtp': {'host': 'smtp.163.com', 'port': 25, 'ssl_port': [465, 994]},
            'imap': {'host': 'imap.163.com', 'port': 143, 'ssl_port': 993},
            'pop3': {'host': 'pop.163.com', 'port': 110, 'ssl_port': 995}
        },
        'yahoo': {
            'smtp': {'host': 'smtp.mail.yahoo.com', 'port': 25, 'ssl_port': [465, 994]},
            # 'imap': {'host': 'imap.163.com', 'port': 143, 'ssl_port': 993},
            'pop3': {'host': 'pop.mail.yahoo.com', 'port': 110, 'ssl_port': 995}
        },
    }


if __name__ == '__main__':
    pass
