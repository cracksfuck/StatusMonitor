#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import logging
import time
from threading import Timer

import psutil
import requests

from client import config

server_addr = config.get_server_addr()
secret = config.get_secret()
name = config.get_name()
location = config.get_location()

__status = {
    'name': name,
    'location': location
}
__last_get = time.time()
__get_interval = 0


def submit_status():
    data = {
        'status': json.dumps(__status)
    }
    headers = {
        'status-secret': secret
    }
    try:
        r = requests.post(server_addr + '/submit_status', data=data, headers=headers)
        if r.status_code != 200:
            logging.error('Error!!! Status Code : %d' % r.status_code)
            return
        res = r.json()
        if not res['success']:
            logging.error('Error!!! msg : ' + res.msg)
        else:
            __status['id'] = int(res['msg'])
    except BaseException as e:
        logging.error(str(e))


def flush_status():
    try:
        now = time.time()
        global __get_interval, __last_get
        __get_interval = now - __last_get
        __last_get = now
        uptime()
        cpu()
        memory()
        swap()
        disk()
        loads()
        net()
    except Exception as e:
        logging.warning('获取系统状态信息失败：' + str(e))
    finally:
        submit_status()
        Timer(1, flush_status).start()


def uptime():
    __status['uptime'] = time.time() - psutil.boot_time()


__last_ct = psutil.cpu_times()


def cpu():
    global __last_ct
    cur_ct = psutil.cpu_times()

    last_total = sum(__last_ct)
    cur_total = sum(cur_ct)

    total = cur_total - last_total
    idle = cur_ct.idle - __last_ct.idle

    percent = (total - idle) / total * 100
    __last_ct = cur_ct
    __status['cpu'] = {
        'percent': percent
    }


def memory():
    mem = psutil.virtual_memory()
    __status['memory'] = {
        'total': mem.total,
        'used': mem.used
    }


def swap():
    swap_mem = psutil.swap_memory()
    __status['swap'] = {
        'total': swap_mem.total,
        'used': swap_mem.used
    }


def disk():
    d = psutil.disk_usage('/')
    __status['disk'] = {
        'total': d.total,
        'used': d.used
    }


def loads():
    load1, load5, load15 = psutil.getloadavg()
    __status['load_1'] = load1
    __status['load_5'] = load5
    __status['load_15'] = load15


__last_net_io = psutil.net_io_counters()


def get_net_tcp_udp_count():
    conns = psutil.net_connections()
    tcp_count = 0
    udp_count = 0
    for conn in conns:
        if conn.type == 1:
            tcp_count += 1
        elif conn.type == 2:
            udp_count += 1
    return tcp_count, udp_count


def net():
    global __last_net_io
    cur_net_io = psutil.net_io_counters()
    sent = cur_net_io.bytes_sent
    recv = cur_net_io.bytes_recv
    up = (sent - __last_net_io.bytes_sent) / __get_interval
    down = (recv - __last_net_io.bytes_recv) / __get_interval
    tcp_count, udp_count = get_net_tcp_udp_count()
    __status['net'] = {
        'io': {
            'up': up,
            'down': down
        },
        'traffic': {
            'sent': sent,
            'recv': recv
        },
        'tcp': {
            'count': tcp_count
        },
        'udp': {
            'count': udp_count
        }
    }
    __last_net_io = cur_net_io


if __name__ == '__main__':
    Timer(1, flush_status).start()
