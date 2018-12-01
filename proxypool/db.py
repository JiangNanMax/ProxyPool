#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/1

# 后续还需要添加异常的处理

import redis

from proxypool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_LIST_NAME

class RedisClient(object):
    '''
    该类实现了连接Redis数据库以及操作数据库中的代理ip列表
    '''
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        """
        建立与Redis数据库的连接
        :param host: Redis数据库的IP地址
        :param port: Redis数据库的端口号
        """
        if REDIS_PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=REDIS_PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    @property
    def list_len(self):
        """
        代理ip列表长度
        :return: 返回列表长度
        """
        return self._db.llen(REDIS_LIST_NAME)

    def flush(self):
        """
        清空Redis数据库中代理ip列表中的所有数据！！！
        """
        self._db.flushdb()

    def put(self, proxy):
        """
        向列表中插入一个代理ip，注意是从列表右端插入
        :param proxy: 待插入的代理ip
        """
        self._db.rpush(REDIS_LIST_NAME, proxy)

    def pop_for_use(self):
        """
        从列表中取出一个代理ip，注意是从列表右端取出，而且取出后该ip就从该列表中删除
        :return: 取出的代理ip
        """
        try:
            return self._db.rpop(REDIS_LIST_NAME)
        except:
            print("Error! when pop")

    def get_for_test(self, num=1):
        """
        获取一定数量的代理ip用于测试，数量默认为1
        :param num: 取出代理ip的数量
        :return: 取出的代理ip
        """
        proxies = self._db.lrange(REDIS_LIST_NAME, 0, num - 1)
        self._db.ltrim(REDIS_LIST_NAME, num, -1)
        return proxies


def test():
    """
    测试函数，用于测试该连接类的功能实现与否
    首先实例化一个RedisClient类，建立与数据库的连接
    然后测试该类中的各个功能函数
    插入数据
    get数据
    pop数据
    刷新数据库中对应的列表

    经多次测试，均正确地实现了工作流程
    """
    redisClient = RedisClient()

    print("Init the client, it's length is {}.".format(redisClient.list_len))

    for i in range(66):
        redisClient.put("{}.{}.{}.{}".format(i, i, i, i))
    print("After put, the length is {}.".format(redisClient.list_len))

    num = 6
    proxies = redisClient.get_for_test(num)
    print("Get {} proxies from client.".format(num))
    for proxy in proxies:
        print(proxy.decode('utf-8'))
    print("After get_for_test, the length is {}.".format(redisClient.list_len))

    print(redisClient.pop_for_use())
    print("After pop_for_use, the length is {}.".format(redisClient.list_len))

    redisClient.flush()
    print("After flush, the length is {}.".format(redisClient.list_len))



if __name__ == '__main__':
    test()
