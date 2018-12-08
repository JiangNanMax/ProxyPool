#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/6

import time
import asyncio
import aiohttp
from multiprocessing import Process
from aiohttp import ClientConnectionError
from proxypool.errors import ProxyResourceDepletionError
from proxypool.db import RedisClient
from proxypool.crawler import FreeProxyCrawler
from proxypool.settings import *


class ValidtyTester(object):
    test_proxy = TEST_PROXY

    def __init__(self):
        self._raw_proxies = None
        self._valid_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')

        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url=self.test_proxy, proxy='http://{}'.format(proxy), timeout=TEST_PROXY_TIMEOUT) as response:
                        if response.status == 200:
                            self._conn.put(proxy)
                            print('Valid proxy: {}'.format(proxy))
                except ClientConnectionError:
                    print('Invalid proxy: {}'.format(proxy))

        except ClientConnectionError as e:
            print(e)

    def test_all_proxies(self):
        print("Running the ValidtyTester...")
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception:
            print("Async error...")


class ProxyPoolAdder(object):
    def __init__(self, upper_threshold):
        self._conn = RedisClient()
        self._crawler = FreeProxyCrawler()
        self._tester = ValidtyTester()
        self._upper_threshold = upper_threshold

    def if_over_upper_threshold(self):
        return self._conn.list_len >= self._upper_threshold

    def add_proxies_to_pool(self):
        print("Running the ProxyPoolAdder...")


class Scheduler(object):
    pass























