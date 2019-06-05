# -*- coding: UTF-8 -*-

import logging
import sys
from configparser import ConfigParser

__sec = 'client'


# 配置文件路径
__config_path = 'client.conf'
__cp = ConfigParser()
try:
    with open(__config_path, 'r') as f:
        __cp.read_string('[%s]\n' % __sec + f.read())
except IOError as e:
    logging.error(__config_path + ' 配置文件读取出错: ' + str(e))
    sys.exit(-1)


def has_option(op):
    return __cp.has_option(__sec, op)


def __get(key, default=None):
    if has_option(key):
        return __cp.get(__sec, key)
    else:
        return default


def get_server_addr():
    addr = __get('server_addr', 'http://127.0.0.1:28288/heihei')
    while addr.endswith('/'):
        addr = addr[0:-1]
    return addr


def get_secret():
    """
    客户端与服务端交互的密码，强烈建议设置一个长随机密码
    :return: 默认 'password'
    """
    return __get('secret', 'password')


def get_name():
    return __get('name', 'test')


def get_location():
    return __get('location', 'Hong Kong')


def get_current_version():
    """
    当前版本
    """
    return '1.0.0'


if __name__ == '__main__':
    for option in __cp.options('sec'):
        print(option + '=' + __cp.get('sec', option))
