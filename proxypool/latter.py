#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/9

# 521错误,也先放弃了。。。
def crawl_66ip(self):
    BASE_PAGE_URL = 'http://www.66ip.cn/{}.html'
    for page in range(1, 4):
        response = requests.get(url=BASE_PAGE_URL.format(page), headers=HEADERS)
        if response.status_code != 200 :
            print('Crawler Error! Status Code: {}'.format(response.status_code))
        else:
            content = PyQuery(response.text)
            '''
            ip_address_re = re.compile('<ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>')
            ip_addresses = ip_address_re.findall(str(content))
            for ip_address, port in ip_addresses:
                proxy = ip_address + ':' + port
                yield proxy
            '''
            print(content)

# 503错误，暂时放弃爬取这个网站吧
def crawl_kuaidaili(self):

    BASE_PAGE_URL = 'https://www.kuaidaili.com/free/inha/{}'
    for page in range(1, 3):
        response = requests.get(url=BASE_PAGE_URL.format(page), headers=HEADERS)
        if response.status_code != 200:
            print('Crawler Error! Status Code: {}'.format(response.status_code))
        else:
            content = response.text
            ip_address_re = re.compile('<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>')
            ip_addresses = ip_address_re.findall(str(content))
            for ip_address, port in ip_addresses:
                proxy = ip_address + ':' + port
                yield proxy