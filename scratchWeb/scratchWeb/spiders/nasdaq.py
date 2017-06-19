# -*- coding: utf-8 -*-
import scrapy
from scratchWeb.items import NasdaqStockPrice

# Usage:scrapy crawl -a symbol=ctrp nasdaq

class NasdaqSpider(scrapy.Spider):
    name = "nasdaq"
    allowed_domains = ["http://www.nasdaq.com"]
    start_urls = []

    def __init__(self, symbol=None, *args, **kwargs):
        super(NasdaqSpider, self).__init__(*args, **kwargs)
        if symbol==None:
            raise ValueError("%s must have a stocke symbol option" % type(self).__name__)
        # 用命令行传入的股票代码拼成URL
        url = "http://www.nasdaq.com/symbol/%s/historical" % (symbol.lower())
        self.start_urls.append(url)

    def parse(self, response):
        filename = 'stock_price.html'
        with open(filename, 'wb') as fd:
            fd.write(response.body)

        # 数据在html表格中,获取表格行数
        table_row = response.xpath("//div[@id='historicalContainer']"
                                   "/div/table/tbody/tr")
        count = len(table_row)
        i = 2
        while i <= count:
            # 解析表格中的每一行,第一行为空,所以从第二行开始
            item = NasdaqStockPrice()
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[1]/text()").extract()
            item["date"] = [s.strip() for s in ret] 
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[2]/text()").extract()
            item["open"] = [s.strip() for s in ret]
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[3]/text()").extract()
            item["high"] = [s.strip() for s in ret]
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[4]/text()").extract()
            item["low"] = [s.strip() for s in ret]
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[5]/text()").extract()
            item["close"] = [s.strip() for s in ret]
            ret = response.xpath("//div[@id='historicalContainer']"
                    "/div/table/tbody/tr[" + str(i) + "]/td[6]/text()").extract()
            item["volume"] = [s.strip() for s in ret]
            i += 1
            yield item

