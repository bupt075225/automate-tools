# -*- coding:utf-8 -*-

import re
import datetime

from orm import DBSession
from orm import HistoricalStockPrices

from data_source import AlphavantageQuery

class Share(object):
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.exchange= "nasdaq"

    def _get_raw_historical_prices(self):
        '''
        从数据源获取历史股价
        '''
        q = AlphavantageQuery(symbol=self.symbol)
        raw_data = q.execute()
        return raw_data

    def _cleanse_raw_data(self, raw_data):
        '''
        清洗从数据源获取到的原始数据,准备写入数据库
        '''
        data = {}
        prices = []
        daily_quote = raw_data["Time Series (Daily)"]
        for k,v in daily_quote.iteritems():
            v_dict = {}
            for key, value in v.iteritems():
                # 清洗dict关键字,例如"1. open"处理后变为"open"
                temp = re.findall("\d+\.\s+(\w+)",key)
                v_dict[temp[0]] = value
            data[k] = v_dict

        for k, v in data.iteritems():
            # 时间字符串转为datetime.date对象
            date = datetime.datetime.strptime(k, "%Y-%m-%d").date()
            price = HistoricalStockPrices(symbol=self.symbol,
                date=date,open=v["open"],high=v["high"],low=v["low"],
                close=v["close"],volume=v["volume"],exchange=self.exchange)
            prices.append(price)

        return prices

    def update_db(self):
        raw_data = self._get_raw_historical_prices()
        historical_prices = self._cleanse_raw_data(raw_data)
        session = DBSession()
        session.add_all(historical_prices)
        session.commit()
        session.close()

    def get_historical(self, start_date, end_date):
        session = DBSession()
        prices = session.query(HistoricalStockPrices).filter(
            HistoricalStockPrices.symbol==self.symbol).filter(
            HistoricalStockPrices.date.between(start_date,end_date)).all()
        session.close()

        output = []
        for price in prices:
            date_dict = {}
            date_dict["date"] = price.date.strftime("%Y-%m-%d")
            date_dict["open"] = price.open
            date_dict["close"] = price.close
            date_dict["high"] = price.high
            date_dict["low"] = price.low
            date_dict["volume"] = price.volume
            date_dict["symbol"] = price.symbol
            output.append(date_dict)

        return output

