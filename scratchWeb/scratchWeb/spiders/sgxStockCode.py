# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest


class SgxstockcodeSpider(scrapy.Spider):
    name = "sgxStockCode"
    allowed_domains = ["www.sgx.com"]
    start_urls = ['http://www.sgx.com/wps/portal/sgxweb_ch/home/company_disclosure/stocks/']

    def star_requests(self):
        for url in start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait':0.5},
            )

    def parse(self, response):
        filename = 'output.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        self.log('Saved file %s' % filename)
