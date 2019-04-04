# -*- coding: utf-8 -*-
BOT_NAME = 'Anjuke'

SPIDER_MODULES = ['Anjuke.spiders']
NEWSPIDER_MODULE = 'Anjuke.spiders'

# LOG_LEVEL = 'WARNING'
# LOG_FILE = './errors_log'
# LOG_FORMAT = '%(asctime)s [%(name)s] %(filename)s %(levelname)s: %(message)s'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# DOWNLOAD_DELAY = 1

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
  'accept-encoding': 'gzip, deflate, br',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'upgrade-insecure-requests': '1',
  'referer': 'https://guangzhou.anjuke.com/',
  ':scheme': 'https',
  ':method': 'GET',
  ':authority': 'gz.zu.anjuke.com'
}


DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"   # 去重类指定
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 调度器
# 持久化，程序关了以后，内容数据保留，下一次启动会继续
SCHEDULER_PERSIST = True

# DOWNLOADER_MIDDLEWARES = {
#     # 'Anjuke.middlewares.ProxyMiddleware': 543,
#     'Anjuke.middlewares.IPProxyDownloadMiddleware': 100,
# }
# MYSQL = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'passwd': '1234',
#     'db': 'anjuke',
#     'charset': 'utf8'
# }

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
# REDIS_PARAMS = {
#     'password':'1234'
# }

#SPIDER_MIDDLEWARES = {
#    'Anjuke.middlewares.AnjukeSpiderMiddleware': 543,
#}


ITEM_PIPELINES = {
  #  'Anjuke.pipelines.AnjukePipeline': 300,
   'Anjuke.pipelines.AnjukeTwistedPipeline': 300,
}
