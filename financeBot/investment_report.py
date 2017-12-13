# -*-coding:utf-8 -*-

from __future__ import division
import sys
import time
import math
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from db import Share
from db import CryptoCurrency

class StockReport(object):
    '''
    股票盈亏报告
    '''
    def __init__(self, symbol, buy_records):
        self.symbol = symbol
        self.buy_records = buy_records

    def _cal_compund_growth_rate(self, data):
        '''
        按照复利计算公式计算投资回报率
        '''
        temp = data['latest_asset']/data['init_asset']
        if 0 != data['index']:
            ratio = round(math.pow(temp, 1.0/data['index']) - 1, 4)
        else:
            ratio = 0
        return ratio

    def _get_stock_data(self, symbol, first_buy_date):
        #从本地数据库获取股票历史价格
        cur_date = time.strftime("%Y-%m-%d" ,time.localtime())
        if symbol=="BTC":
            coin = CryptoCurrency()
            return coin.get_historical_btc(first_buy_date, cur_date)
        elif symbol=="CTRP" or symbol=="FB":
            share = Share(symbol)
            return share.get_historical(first_buy_date, cur_date)
        else:
            raise ValueError("Unknow asset symbol")

    def _get_time_points(self, start, end=time.strftime("%Y-%m-%d" ,time.localtime())):
        '''
        获取统计时间点,买入日期作为之后每月的统计时间点
        '''
        timeSet = []
        startDate = time.strptime(start, "%Y-%m-%d")
        endDate = time.strptime(end, "%Y-%m-%d")
        startDate = datetime.date(startDate.tm_year,startDate.tm_mon,startDate.tm_mday)
        endDate = datetime.date(endDate.tm_year,endDate.tm_mon,endDate.tm_mday)
        dateList = rrule(freq=MONTHLY, dtstart=startDate, until=endDate)
        dateList = [time.strftime("%Y-%m-%d", date.timetuple()) for date in dateList]
        for date in dateList:
            timeSet.append({'date':date})

        return timeSet
        
    def _get_statistic(self, first_buy_date):
        '''
        每月在买入日期查询一次股价,作为当月统计数据
        '''
        data_set = self._get_time_points(first_buy_date)

        historical_data = self._get_stock_data(self.symbol, first_buy_date)
        historicalDict = {}
        for item in historical_data:
            historicalDict[item['date']] = item

        for data in data_set:
            while 1:
                # 统计日期是休市日往前查,找到休市前的第一个交易日
                if not historicalDict.has_key(data['date']):
                    splitDate = data['date'].split('-')
                    next_day = datetime.date(int(splitDate[0]),int(splitDate[1]),int(splitDate[2])) + relativedelta(days=-1)
                    data['date'] = time.strftime('%Y-%m-%d', next_day.timetuple())
                else:
                    break

            data['price'] = historicalDict[data['date']]['close']
        return data_set

    def _get_init_asset(self, buy_records):
        '''
        计算累计投入的现金
        '''
        total_cash = 0
        amount = 0

        for record in buy_records:
            total_cash += record["buy_price"] * record["amount"]
            amount += record["amount"]

        return total_cash, amount

    def ratio_by_year(self):
        '''
        按年计算复利,年复合增长率
        '''
        report = {}
        statistic_values = self._get_statistic(self.buy_records[0]["date"])
        print statistic_values
        start_date = time.strptime(statistic[0]["date"], "%Y-%m-%d")
        end_date = time.strptime(statistic[-1]["date"], "%Y-%m-%d")
        years = end_date.tm_year - start_date.tm_year
        if years < 1:
            data["index"] = 1
        else:
            data["index"] = years
        data = {}
        data["init_asset"], amount = self._get_init_asset(self.buy_records)
        data["latest_asset"] = float(statistic_values[-1]["price"]) * amount
        ratio = self._cal_compund_growth_rate(data)

    def ratio_by_month(self):
        '''
        按月计算复利
        '''
        report = {}
        statistic_values = self._get_statistic(self.buy_records[0]["date"])
        count = len(statistic_values)

        data = {}
        data['init_asset'], amount = self._get_init_asset(self.buy_records)
        i = 0
        while i < count:
            data['latest_asset'] = float(statistic_values[i]['price']) * amount
            data['index'] = i
            ratio = self._cal_compund_growth_rate(data)
            statistic_values[i]['growth_rate_monthly'] = ratio
            statistic_values[i]['symbol'] = self.symbol
            i += 1

        report['detail']=statistic_values
        report['symbol'] = self.symbol
        print report

        return report


if __name__=="__main__":
    import private
    for stock in private.configs['stocks']:
        print stock['symbol']
        report = StockReport(stock['symbol'], stock['buy_records']) 
        ret = report.ratio_by_month()
