#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/1

# 设置Redis数据库连接服务所需要的信息
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_LIST_NAME = 'proxies'

# HTTP请求头部信息
User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
HEADERS = {
    'User-Agent' : User_Agent,
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}

# 设置Flask服务
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
DEBUG = True

# 用于测试代理有效与否的链接
TEST_PROXY = 'http://www.baidu.com'
# 代理测试的时间上限(s)
TEST_PROXY_TIMEOUT = 6

# 代理池中代理ip数量的上限
PROXYPOOL_UPPER_THRESHOLD = 200
# 代理池中代理ip数量的下限
PROXYPOOL_LOWER_THRESHOLD = 20
# 代理池中代理ip数量检查周期(s)
PROXYPOOL_LEN_CHECK_CYCLE = 30
# 代理池中代理ip有效性检查周期(s)
PROXY_VALID_CHECK_CYCLE = 60