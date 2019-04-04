# -*- coding: utf-8 -*-
import scrapy,re
from Anjuke.items import AnjukeItem


class TenementGzSpider(scrapy.Spider):
    name = 'tenement_gz1'
    start_urls = ['https://guangzhou.anjuke.com/']
    page = 1

    def parse(self, response):
        cookies = dict()
        set_cookies = response.headers.getlist('set-cookie')
        for set_cookie in  set_cookies:
            cookie = set_cookie.decode()
            for i in cookie.split('; '):
                cookies[i.split('=')[0]] = i.split('=')[1]
        yield scrapy.Request(
            'https://gz.zu.anjuke.com/fangyuan/p{}-px3/'.format(str(self.page)), 
            callback=self.parse_page, dont_filter=True,cookies=cookies
            )


    def parse_page(self, response):
        print('第%s页' % str(self.page) + '*'*100)
        cookies = dict()
        set_cookies = response.headers.getlist('set-cookie')
        for set_cookie in  set_cookies:
            cookie = set_cookie.decode()
            for i in cookie.split('; '):
                cookies[i.split('=')[0]] = i.split('=')[1]


   
        infos = response.xpath("//div[@class='zu-itemmod  ']")
        for info in infos:
            
            item = AnjukeItem()
            item['city'] = '广州'
            item['link'] = info.xpath("./@link").get()
            item['title'] = info.xpath("./div[@class='zu-info']/h3/a/text()").get()
            zu_info = info.xpath(".//p[@class='details-item tag']//text()").getall()
            # item['house_type'], item['size'] = re.sub("\r|\n|\s|\t","",zu_info[0]), re.sub("\r|\n|\s|\t","",zu_info[2])
            item['floor'] = re.sub("\r|\n|\s|\t","",zu_info[4])
            item['creator'] = re.sub("\r|\n|\s|\t","",zu_info[6]) if len(zu_info) >= 7 else '-'
            address = re.sub("\r|\n|\s|\t|\xa0","",info.xpath(".//address/text()").getall()[-1])
            item['area'], item['street'] = address.split('-')[0], '-'.join(address.split('-')[1:])
            # item['village_name'] = info.xpath(".//address/a/text()").get()
            item['price'] = info.xpath("./div[@class='zu-side']//strong/text()").get()
            # print(item)
            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'item': item}, dont_filter=False)
        
        if self.page > 2:
            self.page == 1
            yield scrapy.Request(
            'https://gz.zu.anjuke.com/fangyuan/px3/',
            callback=self.parse_page, dont_filter=True
        )
        else:
            self.page += 1
            yield scrapy.Request(
                'https://guangzhou.anjuke.com/',
                callback=self.parse, dont_filter=True
            )


    def parse_detail(self, response):
        item = response.meta['item']
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
        item['release_date'] = response.xpath("//div[@class='mod-title bottomed']/div/text()").get().split("：")[1]
        # print(item)
        yield item