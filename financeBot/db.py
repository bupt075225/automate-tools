# -*- coding:utf-8 -*-

import re
import datetime

from sqlalchemy.sql import exists

from orm import DBSession
from orm import HistoricalStockPrices
from orm import HistoricalBtcPrices

from data_source import AlphavantageDataSource
from data_source import CoindeskDataSource


class Share(object):
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.exchange= "nasdaq"

    def _get_raw_historical_prices(self, full=False):
        '''
        从数据源获取历史股价
        '''
        q = AlphavantageDataSource(symbol=self.symbol, full=full)
        raw_data = q.execute()
        return raw_data

    def _cleanse_raw_data(self, raw_data):
        '''
        清洗从数据源获取到的原始数据,准备写入数据库
        '''
        data = {}
        prices = []
        print raw_data
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
            # 有时获取到的原始数有2017-07-03 09:37:00这种时间字符串,用正则式匹配
            date = datetime.datetime.strptime(re.findall("\d+-\d+-\d+",k)[0], 
                    "%Y-%m-%d").date()
            price = HistoricalStockPrices(symbol=self.symbol,
                date=date,open=v["open"],high=v["high"],low=v["low"],
                close=v["close"],volume=v["volume"],exchange=self.exchange)
            prices.append(price)

        return prices

    def _update_db(self, full=False):
        '''
        全量更新和增量更新两种方式,默认增量更新
        '''
        if not full:
            raw_data = self._get_raw_historical_prices()
        else:
            raw_data = self._get_raw_historical_prices(full)

        historical_prices = self._cleanse_raw_data(raw_data)
        session = DBSession()
        for price in historical_prices:
            exist = session.query(
                exists().where(HistoricalStockPrices.date==price.date)
                .where(HistoricalStockPrices.symbol==price.symbol)).scalar()

            if not exist:
                session.add(price)

        session.commit()
        session.close()

    def get_historical(self, start_date, end_date, full=False):
        # 首先更新本地数据库存
        self._update_db(full=full)

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

class CryptoCurrency(object):
    def _get_raw_historical_btc(self, start, end):
        # 从数据源获取历史BTC价格
        source = CoindeskDataSource()
        btc_data = source.get_historical_btc(start,end)
        return btc_data

    def _cleanse_raw_btc(self, raw):
        assert isinstance(raw, dict)

        output = []
        for k,v in raw.iteritems():
            date = datetime.datetime.strptime(k, "%Y-%m-%d").date()
            item = HistoricalBtcPrices(date=date,close=v)
            output.append(item)

        return output

    def _update_db(self, data):
        session = DBSession()
        for price in data:
            exist = session.query(
                exists().where(HistoricalBtcPrices.date==price.date)).scalar()

            # 增量更新
            if not exist:
                session.add(price)

        session.commit()
        session.close()

    def get_historical_btc(self, start_date, end_date):
        # 首先更新本地数据库存
        raw_data = self._get_raw_historical_btc(start_date,end_date)
        data = self._cleanse_raw_btc(raw_data)
        self._update_db(data)

        session = DBSession()
        prices = session.query(HistoricalBtcPrices).filter(
            HistoricalBtcPrices.date.between(start_date,end_date)).all()
        session.close()

        output = []
        for price in prices:
            date_dict = {}
            date_dict["date"] = price.date.strftime("%Y-%m-%d")
            date_dict["close"] = price.close
            output.append(date_dict)

        return output
