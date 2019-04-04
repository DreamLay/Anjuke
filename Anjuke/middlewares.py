# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from datetime import timedelta
import copy
import json
from scrapy import signals


# 代理
class IPProxyDownloadMiddleware(object):
    
    PROXY_URL = 'www.baidu.com'
    CURRENT_PROXY = None
    CURRENT_PROXY_EXPIRE_TIME = None


    def process_request(self, request, spider):
        if 'proxy' not in request.meta or (self.CURRENT_PROXY_EXPIRE_TIME - datetime.now()) < timedelta(seconds=5):
            self.update_proxy()
            request.meta['proxy'] = self.CURRENT_PROXY


    def process_response(self, request, response, spider):
        if response.status != 200: # or 其他形式用不了
            self.update_proxy()
            request.meta['proxy'] = self.CURRENT_PROXY
            return request
        return response


    def update_proxy(self):
        res = requests.get(self.PROXY_URL)
        result = json.loads(res.text)
        data = result['data']
        ip, port, expire_time = data['ip'], data['port'], data['expire_time']
        self.CURRENT_PROXY = "https://{}:{}".format(ip, port)
        date, time = expire_time.split()
        self.CURRENT_PROXY_EXPIRE_TIME = datetime(
            year=date.split('-')[0],
            month=date.split('-')[1],
            day=date.split('-')[2],
            hour=time.split(':')[0],
            minute=time.split(':')[1],
            second=time.split(':')[2]
        )
