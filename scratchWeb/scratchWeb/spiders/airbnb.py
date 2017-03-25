# -*- coding: utf-8 -*-
import scrapy


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    start_urls = ['https://www.airbnb.com/?locale=en/']

    def parse(self, response):
        filename = 'output.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        self.log('Saved file %s' % filename)
