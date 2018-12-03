#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/3

# ip代理池已空的情况
class ProxyPoolEmptyError(Exception):
    def __init__(self):
        super.__init__(self)

    def __str__(self):
        return repr("The Proxy Pool Is Empty!")

# ip代理网站资源爬取完毕的情况
class ProxyResourceDepletionError(Exception):
    def __init__(self):
        super.__init__(self)

    def __str__(self):
        return repr("The Proxy Resource Is Exhausted!")
