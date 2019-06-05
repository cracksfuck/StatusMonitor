# -*- coding: UTF-8 -*-

import logging
import sys
from configparser import ConfigParser

__sec = 'server'


# 配置文件路径
__config_path = 'server.conf'
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


def __get_int(key, default=None):
    if has_option(key):
        return __cp.getint(__sec, key)
    else:
        return default


def get_port():
    """
    服务端监听端口
    :return: 默认 28288
    """
    return __get_int('port', 28288)


def get_secret():
    """
    客户端与服务端交互的密码，强烈建议设置一个长随机密码
    :return: 默认 'password'
    """
    return __get('secret', 'password')


def get_wait_timeout():
    """
    等待客户端最长时间，单位为秒，其作用是，若某个客户端超过这个时间未提交状态信息，则移除这个客户端
    :return: 默认 60
    """
    return __get_int('wait_timeout', 60)


def get_base_path():
    """
    根路径，需以 / 开头
    :return: 默认为空
    """
    base_path = __get('base_path', '')
    if len(base_path) == 0:
        return base_path
    if not base_path.startswith('/'):
        base_path = '/' + base_path
    while base_path.endswith('/'):
        base_path = base_path[0:-1]
    return base_path


def get_cert_file():
    """
    证书文件路径
    :return: 若没有配置，则返回空字符串
    """
    return __get('cert_file', '')


def get_key_file():
    """
    密钥文件路径
    :return: 若没有配置，则返回空字符串
    """
    return __get('key_file', '')


def get_current_version():
    """
    当前版本
    """
    return '1.0.0'


if __name__ == '__main__':
    for option in __cp.options('sec'):
        print(option + '=' + __cp.get('sec', option))
