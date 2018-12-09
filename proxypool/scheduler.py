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

    def is_over_upper_threshold(self):
        return self._conn.list_len >= self._upper_threshold

    def add_proxies_to_pool(self):
        print("Running the ProxyPoolAdder...")
        raw_proxies_count = 0
        while not self.is_over_upper_threshold():
            for callback_type in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_type]
                raw_proxies = self._crawler.get_raw_proxies(callback=callback)
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test_all_proxies()
                raw_proxies_count += len(raw_proxies)
                if self.is_over_upper_threshold():
                    print("Proxies are enough...")
                    break
            if raw_proxies_count == 0:
                raise ProxyResourceDepletionError


class Scheduler(object):
    @staticmethod
    def test_proxies(cycle=PROXY_VALID_CHECK_CYCLE):
        conn = RedisClient()
        tester = ValidtyTester()
        while True:
            print("Testing the validty of proxies...")
            count_to_test = int(0.5 * conn.list_len)
            if count_to_test == 0:
                print("The proxy pool is empty...")
                time.sleep(cycle)
                continue
            raw_proxies = conn.get_for_test(count_to_test)
            tester.set_raw_proxies(raw_proxies)
            tester.test_all_proxies()
            time.sleep(cycle)

    @staticmethod
    def check_pool_len(lower_thershold=PROXYPOOL_LOWER_THRESHOLD, upper_threshold=PROXYPOOL_UPPER_THRESHOLD, cycle=PROXYPOOL_LEN_CHECK_CYCLE):
        conn = RedisClient()
        adder = ProxyPoolAdder(upper_threshold)
        while True:
            if conn.list_len < lower_thershold:
                adder.add_proxies_to_pool()
            time.sleep(cycle)

    def run(self):
        print("Running the scheduler...")
        test_process = Process(target=Scheduler.test_proxies())
        check_process = Process(target=Scheduler.check_pool_len())

        test_process.start()
        check_process.start()