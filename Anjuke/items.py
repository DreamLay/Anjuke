# -*- coding: utf-8 -*-
import scrapy


class AnjukeItem(scrapy.Item):

    price = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    street = scrapy.Field()
    village_name = scrapy.Field()
    house_type = scrapy.Field()
    floor = scrapy.Field()
    size = scrapy.Field()
    aspect = scrapy.Field()
    decoration = scrapy.Field()
    housing_type = scrapy.Field()
    release_date = scrapy.Field()
    title = scrapy.Field()
    creator = scrapy.Field()
    link = scrapy.Field()