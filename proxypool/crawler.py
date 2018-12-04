#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/11/30

class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for key, value in attrs.items():
            if 'crawl_' in key:
                attrs['__CrawlFunc__'].append(key)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyCrawler(object, metaclass=ProxyMetaClass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback: {}'.format(callback))
        for proxy in eval('self.{}'.format(callback)):
            print('Get {} from {}'.format(proxy, callback))
            proxies.append(proxy)
        return proxies

    def crawl_xicidaili(self):
        pass

    def crawl_66ip(self):
        pass

    def crawl_kuaidaili(self):
        pass
