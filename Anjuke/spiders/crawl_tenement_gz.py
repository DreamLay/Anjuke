# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Anjuke.items import AnjukeItem




class CrawlTenementGzSpider(CrawlSpider):
    name = 'tenement_gz'
    # allowed_domains = ['guangzhou.anjuke.com']
    start_urls = [
        'https://gz.zu.anjuke.com/fangyuan/px3/', 
        'https://fs.zu.anjuke.com/fangyuan/px3/',
        'https://sz.zu.anjuke.com/fangyuan/px3/',
        'https://bj.zu.anjuke.com/fangyuan/px3/',
        ]

    rules = (
        Rule(LinkExtractor(allow=r'.+/fangyuan/p\d+-px3/'), follow=True),
        Rule(LinkExtractor(allow=r'.+/fangyuan/\d+'), callback='parse_item', follow=False),
    )
        

    def parse_item(self, response):
        
        item = AnjukeItem()
        city_sim = re.findall(r'https://(.*?).zu.anjuke', response.url)[0]
        if city_sim == 'gz':
            item['city'] = '广州'
        if city_sim == 'sz':
            item['city'] = '深圳'
        if city_sim == 'fs':
            item['city'] = '佛山'
        if city_sim == 'bj':
            item['city'] = '北京'
        lis = response.xpath("//ul[@class='house-info-zufang cf']/li")
        infos = [re.sub("\r|\n|\t|\s","",''.join(li.xpath(".//text()").getall())) for li in lis]
        for info in infos:
            if '小区：' in info:
                item['village_name'] = info.split('小区：')[1]
            if '朝向：' in info:
                item['aspect'] = info.split('朝向：')[1]
            if '装修：' in info:
                item['decoration'] = info.split('装修：')[1]
            if '户型' in info:
                item['house_type'] = info.split('户型：')[1]
            if '面积' in info:
                size = info.split('面积：')[1]
                item['size'] = re.sub('（共[0-9]{0,3}）','',size.replace('平方米', ''))
            if '类型：' in info:
                item['housing_type'] = info.split('类型：')[1]
            if '楼层：' in info:
                item['floor'] = info.split('楼层：')[1]
            # print(info)
        li = response.xpath("//li[@class='house-info-item l-width']/a/text()").getall()
        item['village_name'] = li[0]
        item['area'] = li[1]
        item['street'] = li[2]
        item['release_date'] = response.xpath("//div[@class='mod-title bottomed']/div/text()").get().split("：")[1]
        item['link'] = response.url
        item['title'] = response.xpath("//h3[@class='house-title']/text()").get()
        item['price'] = response.xpath("//span[@class='price']/em/text()").get()
        item['creator'] = response.xpath("//h2[@class='broker-name']/text()").get()
        yield item