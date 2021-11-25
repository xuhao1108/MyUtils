#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : 获取电脑相关信息
import wmi
import hashlib

__all__ = ['get_cpu_info', 'get_disk_info', 'get_network_info', 'get_mainboard_info', 'generate_driver_id']

my_wmi = wmi.WMI()


def get_cpu_info():
    """
    cpu
    """
    cpu = []
    for info in my_wmi.Win32_Processor():
        cpu.append(
            {
                'name': info.Name,
                'serial_number': info.ProcessorId,
                'core_num': info.NumberOfCores
            }
        )
    return cpu


def get_disk_info():
    """
    硬盘
    """
    disk = []
    for info in my_wmi.Win32_DiskDrive():
        disk.append(
            {
                'serial': my_wmi.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),
                'id': info.deviceid,
                'caption': info.Caption,
                'size': str(int(float(info.Size) / 1024 / 1024 / 1024)) + 'G'
            }
        )
    return disk


def get_network_info():
    """
    网络
    """
    network = []
    for info in my_wmi.Win32_NetworkAdapterConfiguration():
        if info.MACAddress is not None:
            network.append(
                {
                    'mac': info.MACAddress,  # 无线局域网适配器、WLAN、物理地址
                    'ip': info.IPAddress
                }
            )
    return network


def get_mainboard_info():
    """
    主板序列号
    """
    mainboard = []
    for info in my_wmi.Win32_BaseBoard():
        mainboard.append(info.SerialNumber.strip().strip('.'))
    return mainboard


def md5(data_str, encoding='utf-8'):
    """
    字符转md5
    """
    m = hashlib.md5()
    m.update(data_str.encode(encoding))
    return m.hexdigest()


def generate_driver_id():
    """
    生成每个电脑唯一的机器码
    """
    for info in my_wmi.Win32_DiskDrive():
        if info.index == 0:
            serial = info.SerialNumber if info.SerialNumber else 'default'
            mac = my_wmi.Win32_NetworkAdapterConfiguration(IPEnabled=1)[0].MACAddress
            return md5(serial + info.Caption + info.Size + mac)


if __name__ == '__main__':
    pass
