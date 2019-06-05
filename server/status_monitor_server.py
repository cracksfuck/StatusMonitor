#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import logging
import os
import random
import sys
import time
from threading import Timer

import tornado.log
from flask import Flask, render_template, jsonify, request
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import config

port = config.get_port()
secret = config.get_secret()
wait_timeout = config.get_wait_timeout()
base_path = config.get_base_path()
cert_file = config.get_cert_file()
key_file = config.get_key_file()


app = Flask(__name__, static_folder='', static_url_path='')
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.secret_key = os.urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 6307200
cur_version = config.get_current_version()

__statuses = {}


@app.route(base_path + '/', methods=['GET'])
def index():
    return render_template('index.html', base_path=base_path, cur_version=cur_version)


@app.route(base_path + '/statuses', methods=['POST'])
def statuses():
    return jsonify(list(__statuses.values()))


@app.route(base_path + '/submit_status', methods=['POST'])
def submit_status():
    try:
        secret_client = request.headers['status-secret']
        if secret != secret_client:
            return jsonify({'success': False, 'msg': 'Secret Wrong'})
        status = json.loads(request.form['status'])
        if 'id' not in status:
            id = random.randint(1, 1000000000)
            while id in __statuses:
                id = random.randint(1, 1000000000)
            status['id'] = id
        else:
            id = status['id']
        status['submit_time'] = time.time()
        __statuses[id] = status
        return jsonify({'success': True, 'msg': id})
    except Exception as e:
        logging.warning(str(e))
        return jsonify({'success': False, 'msg': 'Server Error: ' + str(e)})


def kick_client_job():
    now = time.time()
    try:
        for k in list(__statuses.keys()):
            status = __statuses[k]
            if now - status['submit_time'] > wait_timeout:
                del __statuses[k]
    except Exception as e:
        logging.warning(str(e))
    finally:
        Timer(wait_timeout, kick_client_job).start()


def get_ssl_option():
    """
    获取 ssl 配置
    :return: 如配置了证书和密钥路径，则返回配置信息，否则返回 None
    """
    if cert_file != '' and key_file != '':
        return {
            'certfile': cert_file,
            'keyfile': key_file
        }
    return None


def main():
    print('启动中...')
    tornado.log.access_log.setLevel('ERROR')
    tornado.log.app_log.setLevel('ERROR')
    tornado.log.gen_log.setLevel('ERROR')
    http_server = HTTPServer(WSGIContainer(app), ssl_options=get_ssl_option())
    http_server.listen(port)
    print("启动完毕，监听端口为 %d" % port)
    IOLoop.current().start()


if __name__ == '__main__':
    try:
        Timer(wait_timeout, kick_client_job).start()
        main()
    except BaseException as e:
        logging.error('启动失败，请查看报错信息：')
        logging.error(str(e))
        sys.exit(-1)
