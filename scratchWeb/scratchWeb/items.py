# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join


class AirbnbListing(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    accommodates = scrapy.Field()
    property_type = scrapy.Field()
    room_type = scrapy.Field()
    min_stay = scrapy.Field()
    reviews = scrapy.Field()
    rank = scrapy.Field()
    host_since = scrapy.Field()
    neighbourhood = scrapy.Field()
    url = scrapy.Field()


class AirbnbListingLoader(ItemLoader):
    default_output_processor = Identity()
    neighbourhood_out = Join()
    min_stay_out = Join()

class NasdaqStockPrice(scrapy.Item):
    symbol = scrapy.Field()
    date = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()

class LagouJob(scrapy.Item):
    company_name = scrapy.Field()
    position_name = scrapy.Field()
    release_time = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_address = scrapy.Field()
    finance_stage = scrapy.Field()
    industry_field = scrapy.Field()
    company_size = scrapy.Field()
    education = scrapy.Field()

class LianjiaErShouFang(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    house_style = scrapy.Field()
    house_area = scrapy.Field()
    inline_area = scrapy.Field()
    building_time = scrapy.Field()
    decoration = scrapy.Field()
    property_years = scrapy.Field()
    floor = scrapy.Field()
    register_date = scrapy.Field()
    view_count = scrapy.Field()
    neighborhoods = scrapy.Field()

class LianjiaErShouFangLoader(ItemLoader):
    default_output_processor = Identity()
    neighborhoods_out = Join()
