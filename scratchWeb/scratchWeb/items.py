# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class airbnb_listing(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    accommodates = scrapy.Field()
    property_type = scrapy.Field()
    room_type = scrapy.Field()
    min_stay = scrapy.Field()
    reviews = scrapy.Field()
    rank = scrapy.Field()
    host_since = scrapy.Field()
    url = scrapy.Field()


