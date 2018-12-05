#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/5

from flask import Flask, g
from proxypool.settings import FLASK_HOST, FLASK_PORT, DEBUG
from proxypool.db import RedisClient


def conn_to_redis():
    """
    判断当前全局是否实例化Redis连接类，已实例化则直接返回该对象，否则进行实例化后返回
    :return: 实例化的Redis连接类
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client

# 创建一个Flask应用
app = Flask(__name__)

# 简易页面
home_page = """
                <h2>JiangNanMax's ProxyPool</h2>
                <a href="http://0.0.0.0:5000/count">Proxy's count</a>
                <br>
                <br>
                <a href="http://0.0.0.0:5000/get">GET an ip for use</a>
            """

# 设置路由
# 主要就是三个页面，首页、当前Redis中的代理数量、从Redis中取出一个代理

@app.route('/')
def index():
    return home_page


@app.route('/count')
def get_count():
    conn = conn_to_redis()
    return str(conn.list_len)


@app.route('/get')
def get_proxy():
    conn = conn_to_redis()
    return conn.pop_for_use()


def test():
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)


if __name__ == '__main__':
    test()