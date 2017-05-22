# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scratchWeb.items import airbnb_listing


class AirbnbSpider(CrawlSpider):
    name = "airbnb"
    allowed_domains = ['airbnbchina.cn']
    start_urls = ['https://www.airbnbchina.cn']

    def parse_start_url(self, response):
        # 搜索指定城市的房源
        return scrapy.FormRequest.from_response(response, 
            formxpath="//form/div[@class='SearchForm__inputs-wrapper col-md-12']",
            formdata={'location': '上海'},
            callback=self.browse_rooms
        )

    def follow_links(self, response):
        next_page_link = response.xpath("//li[@class='next next_page']/a/@href").extract()
        links = LinkExtractor(allow=("/rooms/\d+\?location=.*",)).extract_links(response)
        return links,next_page_link

    def browse_rooms(self, response):
        '''
        filename = 'output.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        self.log('Saved file %s' % filename)
        '''

        room_links,next_page = self.follow_links(response)
        for link in room_links:
            print "Request %s..." % link.url
            yield scrapy.Request(link.url, callback=self.parse_room_info)
            #return scrapy.Request(link.url, callback=self.parse_room_info)

        if len(next_page)!=0:
            print "Go to next page......"
            yield scrapy.Request(self.start_urls[0] + next_page[0], callback=self.browse_rooms)
            #return scrapy.Request(self.start_urls[0] + next_page[0], callback=self.browse_rooms)
        else:
            yield []
            #return []

    def parse_room_info(self, response):
        '''
        self.log("This is a room page %s" % response.url)
        filename = 'room.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        '''

        listing = airbnb_listing()
        listing["accommodates"] = response.xpath(u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '可住')]/strong/text()").extract()
        listing["room_type"] = response.xpath(u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '房间类型')]/strong/text()").extract()
        listing["property_type"] = response.xpath(u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '房源类型')]/a/strong/text()").extract()
        listing["min_stay"] = response.xpath(u"//div[contains(., '最短住宿晚数')]"
                     u"/strong/text()").extract()
        listing["reviews"] = response.xpath("//h4[contains(@class,'review-header-text')]"
                     "/span/span/text()").extract()
        listing["rank"] = response.xpath("//h4[contains(@class,'review-header-text')]"
                     "/div/div/@aria-label").extract()
        listing["host_since"] = response.xpath(u"//span/span[contains(., '注册时间')]"
                     u"/text()").extract()
        listing["url"] = response.url

        print listing.items()
        return listing

