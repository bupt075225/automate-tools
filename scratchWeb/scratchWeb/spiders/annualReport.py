# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AnnualreportSpider(CrawlSpider):
    name = "annualReport"
    allowed_domains = ["google.com"]
    start_urls = ['http://google.com/']

    def parse_item(self, response):
        pass
