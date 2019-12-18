# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlLianjiaSingleItem(scrapy.Item):
    # define the fields for your item here like:
    houseinfo1 = scrapy.Field()
    houseinfo2 = scrapy.Field()
    dealdate = scrapy.Field()
    totalprice = scrapy.Field()
    floor = scrapy.Field()
    unitprice = scrapy.Field()

    pass
