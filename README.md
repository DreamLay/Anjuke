# 爬取anju客租房信息（异步入库及ip代理池）


### 一、关于异步
    
1. scrapy默认使用Twisted异步爬取数据，类似但不同于python多线程。

2. pipleline中入库时是同步执行的，当爬虫增多数据量大时对性能有不小影响，故改用twisted异步入库。


### 二、关于代理池

1. anju客检测到同一ip请求多次会重定向到滑动验证码界面。

2. 用的是芝麻代理，返回数据格式
```json
{
    "code":0,
    "success":true,
    "msg":"0",
    "data":[
        {
            "ip":"49.68.68.197",
            "port":33220,
            "expire_time":"2017-06-20 20:40:24",
            "city":"徐州市",
            "isp":"电信"
        }
    ]
}
```
3. 增加下载中间件，判断匿名ip过期时间以及ip是否被黑自动重新请求代理并替换

> 注：settings中未启用，需要自行购买代理并修改如下代码

```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    # 'Anjuke.middlewares.ProxyMiddleware': 543,
    'Anjuke.middlewares.IPProxyDownloadMiddleware': 100,
}

# middlewares.py
class IPProxyDownloadMiddleware(object):

    PROXY_URL = 'www.baidu.com'  # 修改为ip提取地址
    CURRENT_PROXY = None
    CURRENT_PROXY_EXPIRE_TIME = None
```