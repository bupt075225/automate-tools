# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join


class AirbnbListing(scrapy.Item):
    # 价格
    price = scrapy.Field()
    # 可住几人
    accommodates = scrapy.Field()
    # 房间类型
    property_type = scrapy.Field()
    # 房屋类型
    room_type = scrapy.Field()
    # 最少住几晚
    min_stay = scrapy.Field()
    # 评论数
    reviews = scrapy.Field()
    # 星级排名/最多5星
    rank = scrapy.Field()
    # 注册时间
    host_since = scrapy.Field()
    # 所在街区
    neighbourhood = scrapy.Field()
    # 房源详情页面的URL
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
    # 公司名称
    company_name = scrapy.Field()
    # 职位名称
    position_name = scrapy.Field()
    # 发布时间
    release_time = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 所在城市
    city = scrapy.Field()
    # 工作地址
    work_address = scrapy.Field()
    # 发展阶段
    finance_stage = scrapy.Field()
    # 所属领域
    industry_field = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()
    # 求职者教育程度
    education = scrapy.Field()

class LianjiaErShouFang(scrapy.Item):
    # 所在小区的名字
    title = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 每平米单价
    unit_price = scrapy.Field()
    # 户型/几居室
    house_style = scrapy.Field()
    # 建面
    house_area = scrapy.Field()
    # 套内面积
    inline_area = scrapy.Field()
    # 修建时间
    building_time = scrapy.Field()
    # 装修程度
    decoration = scrapy.Field()
    # 产权年限
    property_years = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 挂牌时间
    register_date = scrapy.Field()
    # 近一周内看房次数
    view_count = scrapy.Field()
    # 所在区域
    neighborhoods = scrapy.Field()

class LianjiaErShouFangLoader(ItemLoader):
    default_output_processor = Identity()
    neighborhoods_out = Join()
