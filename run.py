#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,sys
from Anjuke import settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from Anjuke.spiders import tenement_gz


def main():
    
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl(tenement_gz.TenementGzSpider)
    process.start()


if __name__ == '__main__':
    main()