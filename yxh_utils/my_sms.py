#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 16:43
# @Author : 闫旭浩
# @Email : 874591940@qq.com
# @desc : ...
import requests

__all__ = ['YxhSmsActivate']


class YxhSmsActivate(object):
    def __init__(self, api_key):
        """
        详细参数请查看：https://sms-activate.ru/cn/api2#apiStandart
        :param api_key: API密钥
        """
        self.url = 'https://api.sms-activate.org/stubs/handler_api.php'
        self.api_key = api_key
        self.ref = 1648994
        self.session = requests.Session()
        self.session.trust_env = False

    def get_request_data(self, params):
        """
        获取请求结果
        :param params: 请求参数
        :return:
        """
        response = self.session.get(self.url, params=params, timeout=30)
        try:
            return response.json()
        except:
            return response.text

    def get_numbers_status(self, operator=None, country=0):
        """
        查询可供使用号码数量
        :param operator: 移动运营商号码
            俄罗斯	megafon,mts,beeline,tele2,any
            乌克兰	kyivstar,life,utel,mts,vodafone
            哈萨克斯坦	tele2,beeline,aktiv,altel
        :param country: 号码的国家
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getNumbersStatus',
            'country': country,
        }
        if operator:
            params['operator'] = ','.join(operator) if isinstance(operator, list) else operator
        return self.get_request_data(params)

    def get_top_countries_by_service(self, service, free_price=False):
        """
        按服务请求顶级国家/地区
        :param service: 服务
        :param free_price: 数量和价格将根据免费价格转移
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getTopCountriesByService',
            'service': service,
            'freePrice': free_price,
        }

        return self.get_request_data(params)

    def get_balance(self):
        """
        询问余额
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getBalance',
        }
        data = self.get_request_data(params)
        try:
            return data.split(':')[-1]
        except:
            return data

    def get_balance_and_cashback(self):
        """
        号余额及返现账户余额查询
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getBalanceAndCashBack',
        }
        return self.get_request_data(params)

    def get_number(self, service, forward=None, free_price=False, max_price=10, phone_exception=None, operator=None, country=0):
        """
        号码订单
        :param service: 服务
        :param forward: 可选参数，以逗号分隔指定转发字符，转发位数必须与参数中传输的服务数量匹配。是否有必要申请呼叫转移号码：0 - 不执行；1 - 执行
        :param free_price: 使用免费价格购买号码
        :param max_price: 准备以免费价格购买的最高价格
        :param phone_exception: 不包括俄语数字的前缀。用逗号指定。记录格式：国家代码和掩码的3到6位数字（例如7918,7900111）。
        :param operator: 移动运营商号码，您可以指定多个以逗号分隔的号码
        :param country: 号码的国家
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getNumber',
            'service': service,
            'freePrice': free_price,
            'ref': self.ref,
            'country': country,
        }
        if forward:
            params['forward'] = forward
        if free_price:
            params['maxPrice'] = max_price
        if phone_exception:
            params['phoneException'] = phone_exception
        if operator:
            params['operator'] = ','.join(operator) if isinstance(operator, list) else operator

        data = self.get_request_data(params)
        try:
            info = data.split(':')
            return {
                'id': info[1],
                'number': info[2]
            }
        except:
            return data

    def get_multi_service_number(self, service, forward=None, operator=None, country=0):
        """
        订购多个服务的电话号码
        :param service: 订购服务。指定用逗号分隔的名称
        :param forward: 可选参数，以逗号分隔指定转发字符，转发位数必须与参数中传输的服务数量匹配。是否有必要申请呼叫转移号码：0 - 不执行；1 - 执行
        :param operator: 移动运营商号码
            俄罗斯	megafon,mts,beeline,tele2,any
            乌克兰	kyivstar,life,utel,mts,vodafone
            哈萨克斯坦	tele2,beeline,aktiv,altel
        :param country: 号码的国家
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getMultiServiceNumber',
            'multiService': ','.join(service) if isinstance(service, list) else service,
            'ref': self.ref,
            'country': country,
        }
        if forward:
            params['multiForward'] = forward
        if operator:
            params['operator'] = ','.join(operator) if isinstance(operator, list) else operator
        data = self.get_request_data(params)
        try:
            result = {}
            for item in data:
                # name = item['service']
                # if name not in result:
                #     result[name] = []
                # result[name].append({'id': item['phone'], 'number': item['activation']})
                result[item['service']] = {'id': item['phone'], 'number': item['activation']}
            return result
        except:
            return data

    def set_status(self, _id, status, forward=None):
        """
        激活状态的修改
        :param _id:
        :param status: 激活状态
            1	通知关于号码的准备状态 （短信被发送）
            3	再次询问密码（免费）
            6	完全激活*
            8	通知关于使用号码而取消激活
        :param forward: 要重定向到的电话号码
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': _id,
            'status': status,
        }
        if forward:
            params['forward'] = forward
        return self.get_request_data(params)

    def get_status(self, _id):
        """
        请通知关于激活状态
        :param _id:
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getStatus',
            'id': _id,
        }
        return self.get_request_data(params)

    def get_prices(self, service, country):
        """
        收到各国家现实的价格
        :param service: 服务
        :param country: 国家
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getPrices',
            'service': service,
            'country': country,
        }
        return self.get_request_data(params)

    def get_countries(self):
        """
        获取所有国家的清单
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getCountries',
        }
        return self.get_request_data(params)

    def get_additional_service(self, service, _id):
        """
        重定向号码的附加服务
        :param service: 服务
        :param _id:
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getAdditionalService',
            'service': service,
            'id': _id,
        }
        return self.get_request_data(params)

    def get_rent_services_and_countries(self, rent_time=60 * 60 * 1, operator=None, country=0):
        """
        请求可用的国家和服务
        :param rent_time: 出租时间。默认值为1小时。
        :param operator: 移动运营商号码，您可以指定多个以逗号分隔的号码
        :param country: 国家（默认：俄罗斯）
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getRentServicesAndCountries',
            'rent_time': rent_time,
            'country': country,
        }
        if operator:
            params['operator'] = ','.join(operator) if isinstance(operator, list) else operator
        return self.get_request_data(params)

    def get_rent_number(self, service, rent_time=60 * 60 * 4, operator=None, country=0, webhook=None):
        """
        房间预订出租
        :param service: 服务
        :param rent_time: 租用时间（默认：4小时）
        :param operator: 移动运营商号码
        :param country: 国家（默认：俄罗斯）
        :param webhook: webhook的链接（默认情况下不考虑）
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getRentNumber',
            'service': service,
            'rent_time': rent_time,
            'country': country,
        }
        if operator:
            params['operator'] = ','.join(operator) if isinstance(operator, list) else operator
        if webhook:
            params['url'] = webhook
        return self.get_request_data(params)

    def set_rent_status(self, _id, status):
        """
        租赁状态变更
        :param _id: 订购房间时在响应中收到的租金ID
        :param status: 更改状态的代码
            1	终点线
            2	取消
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'setRentStatus',
            'id': _id,
            'status': status,
        }
        return self.get_request_data(params)

    def get_rent_status(self, _id):
        """
        获取租金状态
        :param _id: 订购房间时在响应中收到的租金ID
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getRentStatus',
            'id': _id,
        }
        return self.get_request_data(params)

    def get_rent_list(self):
        """
        列出当前激活
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getRentList'
        }
        return self.get_request_data(params)

    def continue_rent_number(self, _id, rent_time=60 * 60 * 4):
        """
        获取租金状态
        :param _id: 订购房间时在响应中收到的租金ID
        :param rent_time: 租用时间（默认：4小时）
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'continueRentNumber',
            'id': _id,
            'rent_time': rent_time,
        }
        return self.get_request_data(params)

    def get_continue_rent_price_number(self, _id):
        """
        获取续约费用
        :param _id: 订购房间时在响应中收到的租金ID
        :return:
        """
        params = {
            'api_key': self.api_key,
            'action': 'getContinueRentPriceNumber',
            'id': _id,
        }
        return self.get_request_data(params)


if __name__ == '__main__':
    pass
