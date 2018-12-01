#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/1

import redis

from proxypool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_LIST_NAME

class RedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        if REDIS_PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=REDIS_PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    @property
    def list_len(self):
        return self._db.llen(REDIS_LIST_NAME)

    def flush(self):
        self._db.flushall()

    def put(self, proxy):
        self._db.rpush(REDIS_LIST_NAME, proxy)

    def pop_for_use(self):
        try:
            return self._db.rpop(REDIS_LIST_NAME)
        except:
            print("Error! when pop")

    def get_for_test(self, num=1):
        proxies = self._db.lrange(REDIS_LIST_NAME, 0, num - 1)
        self._db.ltrim(REDIS_LIST_NAME, num, -1)
        return proxies


def main():
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
    main()










