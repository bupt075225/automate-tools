# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scratchWeb.items import LianjiaErShouFang, LianjiaErShouFangLoader


class LianjiaSpiderSpider(CrawlSpider):
    name = "lianjia_spider"
    allowed_domains = ["lianjia.com"]
    start_urls = ['http://cd.lianjia.com/ershoufang']

    # 从二手房列表中提取房源详情页面URL链接
    ershoufang_link_extractor = LinkExtractor(allow="https://cd.lianjia.com/ershoufang/" + "\d+\.html", 
        restrict_xpaths="//ul[@class='sellListContent']")
    rules = (Rule(ershoufang_link_extractor, 
                  callback="parse_ershoufang", 
                  follow=True),
            )

    def parse_start_url(self, response):
        '''
        提取二手房搜索结果的下一页链接
        '''
        page_data = response.xpath(
            "//div[@class='page-box house-lst-page-box']/@page-data").extract()
        match = re.findall(":(\d+)", page_data[0])
        total_page = int(match[0])
        cur_page = int(match[1])
        next_page = cur_page + 1
        if next_page <= total_page:
            next_page_url = self.start_urls[0] + "/pg" + str(next_page)
            # 不设置callback参数,scrapy会使用Spider类的parse方法作为响应回调,
            # CrawlSpider子类的parse方法会调用parse_start_url
            return scrapy.Request(next_page_url)
        else:
            return []

    def parse_ershoufang(self, response):
        '''
        从二手房详情页面提取信息
        '''

        item_loader = LianjiaErShouFangLoader(item=LianjiaErShouFang(),
            response=response)

        item_loader.add_xpath("title",
            "//div[@class='communityName']/a[@class='info']/text()")
        item_loader.add_xpath("price",
            "//div[@class='price ']/span[@class='total']/text()")
        item_loader.add_xpath("unit_price",
            "//div[@class='unitPrice']/span[@class='unitPriceValue']/text()")
        item_loader.add_xpath("house_style",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[1]/text()")
        item_loader.add_xpath("house_area",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[3]/text()")
        item_loader.add_xpath("inline_area",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[5]/text()")
        item_loader.add_xpath("building_time",
            "//div[@class='content']/div[@class='houseInfo']/div[@class='area']/div[@class='subInfo']/text()")
        item_loader.add_xpath("decoration",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[9]/text()")
        item_loader.add_xpath("property_years",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[12]/text()")
        item_loader.add_xpath("floor",
            "//div[@class='introContent']/div[@class='base']/div[@class='content']/ul/li[2]/text()")
        item_loader.add_xpath("register_date",
            "//div[@class='introContent']/div[@class='transaction']/div[@class='content']/ul/li[1]/text()")
        item_loader.add_xpath("view_count",
            "//div[@id='record']/div[@class='panel']/div[@class='count']/text()")
        item_loader.add_xpath("neighborhoods",
            "//div[@class='areaName']/span[@class='info']/a/text()"
            " | //div[@class='areaName']/span[@class='info']/text()")

        return item_loader.load_item()


