# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scratchWeb.items import AirbnbListing, AirbnbListingLoader


class AirbnbSpider(CrawlSpider):
    name = "airbnb"
    allowed_domains = ['airbnbchina.cn']
    start_urls = ['https://www.airbnbchina.cn']

    def parse_start_url(self, response):
        # 搜索指定城市的房源,提交搜索表单
        return scrapy.FormRequest.from_response(response, 
            formxpath="//form/div[@class='SearchForm__inputs-wrapper col-md-12']",
            formdata={'location': '上海'},
            callback=self.browse_rooms
        )

    def _follow_links(self, response):
        # 提取房源列表中每个房源链接和列表下一页链接
        next_page_link = response.xpath("//li[@class='next next_page']/a/@href").extract()
        links = LinkExtractor(allow=("/rooms/\d+\?location=.*",)).extract_links(response)
        return links,next_page_link

    def browse_rooms(self, response):
        # 发起对房源详情页面的请求
        room_links,next_page = self._follow_links(response)
        for link in room_links:
            print "Request %s..." % link.url
            #yield scrapy.Request(link.url, callback=self.parse_room_info)
            yield scrapy.Request(link.url, callback=self.parse_room_info, meta={
                    "splash":{
                        "args": {
                            "wait":0.5,
                            "timeout":60,
                        },
                        "endpoint":"render.html",
                    }
                })

        if len(next_page)!=0:
            print "Go to next page......"
            yield scrapy.Request(self.start_urls[0] + next_page[0], callback=self.browse_rooms)
            #return scrapy.Request(self.start_urls[0] + next_page[0], callback=self.browse_rooms)
        else:
            yield []
            #return []


    def parse_room_info(self, response):
        # 房源页面响应回调函数,提取房源信息
        self.log("This is a room page %s" % response.url)
        '''
        filename = 'room.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)
        '''

        item_loader = AirbnbListingLoader(item=AirbnbListing(),
                                  response=response)
        item_loader.add_xpath("price", u"//span[@class='priceAmountWrapper_17axpax']"
                     u"/span/span/text()")
        item_loader.add_xpath("accommodates", u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '可住')]/strong/text()")
        item_loader.add_xpath("room_type", u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '房间类型')]/strong/text()")
        item_loader.add_xpath("property_type", u"//div[@class='bottom-spacing-2']"
                     u"/div[contains(., '房源类型')]/a/strong/text()")
        item_loader.add_xpath("min_stay", u"//div[contains(., '最短住宿晚数')]"
                     u"/strong/text()")
        item_loader.add_xpath("reviews", "//h4[contains(@class,'review-header-text')]"
                     "/span/span/text()")
        item_loader.add_xpath("rank", "//h4[contains(@class,'review-header-text')]"
                     "/div/div/@aria-label")
        item_loader.add_xpath("host_since", u"//span/span[contains(., '注册时间')]"
                     u"/text()")
        item_loader.add_xpath("neighbourhood", "//div[@id='neighborhood']"
          "/descendant::span[@class='listing-location']/descendant-or-self::span/text()")
        item_loader.add_value("url", response.url)

        return item_loader.load_item()

