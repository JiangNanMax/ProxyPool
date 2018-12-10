#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/11/30

import requests
import re
from pyquery import PyQuery
from proxypool.settings import HEADERS


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
        for proxy in eval('self.{}()'.format(callback)):
            print('Get {} from {}'.format(proxy, callback))
            proxies.append(proxy)
        return proxies

    #正常
    def crawl_xicidaili(self):
        BASE_PAGE_URL = 'http://www.xicidaili.com/wt/{}'
        for page in range(1, 4):
            response = requests.get(url=BASE_PAGE_URL.format(page), headers=HEADERS)
            if response.status_code != 200 :
                print('Crawler Error! Status Code: {}'.format(response.status_code))
            else:
                content = response.text
                ip_address_re = re.compile('<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                ip_addresses = ip_address_re.findall(str(content))
                for ip_address, port in ip_addresses:
                    proxy = ip_address + ':' + port
                    yield proxy

    #正常
    def crawl_data5u(self):
        BASE_PAGE_URL = 'http://www.data5u.com/free/{}/index.shtml'
        for page in ['gngn', 'gnpt', 'gwgn', 'gwpt']:
            response = requests.get(url=BASE_PAGE_URL.format(page), headers=HEADERS)
            if response.status_code != 200 :
                print('Crawler Error! Status Code: {}'.format(response.status_code))
            else:
                content = response.text
                ip_address_re = re.compile('<ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>')
                ip_addresses = ip_address_re.findall(str(content))
                for ip_address, port in ip_addresses:
                    proxy = ip_address + ':' + port
                    yield proxy




def test():
    crawler = FreeProxyCrawler()
    print(crawler.__CrawlFuncCount__)
    for ip in crawler.crawl_xicidaili():
        print(ip)
    for ip in crawler.crawl_data5u():
        print(ip)


if __name__ == '__main__':
    test()
