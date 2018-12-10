#!/usr/bin/python
# -*- coding utf-8 -*-
# Project: ProxyPool
# Author: jiangnan 
# Mail: jiangnanmax@gmail.com
# Date: 2018/12/9

from proxypool.flask_service import app
from proxypool.scheduler import Scheduler
from proxypool.settings import FLASK_HOST, FLASK_PORT


if __name__ == '__main__':
    s = Scheduler()
    s.run()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
