# -*-coding:utf-8 -*-

from __future__ import division
import sys
import time
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from db import Share
from db import CryptoCurrency

class StockReport(object):
    '''
    股票盈亏报告
    '''
    def __init__(self, symbol, buy_date, price, count):
        self.symbol = symbol
        self.buy_date = buy_date
        self.buy_price = price
        self.count = count

    def _profit_ratio(self, data):
        '''
        计算每月收益率
        '''
        lastAsset = float(data['lastPrice']) * data['number']
        latestAsset = float(data['latestPrice']) * data['number']
        lastAsset = round(lastAsset,2)
        latestAsset = round(latestAsset,2)

        percent = ((latestAsset - lastAsset) / lastAsset) * 100
        return (str(round(percent, 2)) + '%')

    def _get_stock_data(self, symbol):
        #从本地数据库获取股票历史价格
        cur_date = time.strftime("%Y-%m-%d" ,time.localtime())
        if symbol=="BTC":
            coin = CryptoCurrency()
            return coin.get_historical_btc(self.buy_date, cur_date)
        else:
            share = Share(symbol)
            return share.get_historical(self.buy_date, cur_date)

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
        
    def _get_statistic(self):
        '''
        每月在买入日期查询一次股价,作为当月统计数据
        '''
        data_set = self._get_time_points(self.buy_date)

        historical_data = self._get_stock_data(self.symbol)
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

    def ratio_by_month(self):
        report = {}
        statistic_values = self._get_statistic()
        count = len(statistic_values)
        i = 0
        data = {}
        statistic_values[0]['symbol'] = self.symbol
        statistic_values[0]['growth_rate'] = 0
        while i < (count - 1):
            j = i + 1
            data['lastPrice'] = statistic_values[i]['price']
            data['latestPrice'] = statistic_values[j]['price']
            data['number'] = self.count
            ratio = self._profit_ratio(data)
            statistic_values[j]['growth_rate'] = ratio
            statistic_values[j]['symbol'] = self.symbol
            i += 1
        report['detail']=statistic_values
        report['symbol'] = self.symbol

        if count > 1:
            data['lastPrice'] = self.buy_price
            data['latestPrice'] = statistic_values[-1]['price']
            data['number'] = self.count
            ratio = self._profit_ratio(data)
            print 'Latest date %s ratio:' % statistic_values[-1]['date']
            print ratio
            report['growth_rate'] = ratio
        else:
            report['info'] = 'There is only the first month statistic data found'
            report['growth_rate'] = 0

        return report


if __name__=="__main__":
    if len(sys.argv) != 5:
        print "usage: python %s symbol date price count" % sys.argv[0]
        print "       symbol: 股票代码"
        print "       date  : 买入日期,示例：2016-12-15"
        print "       price : 买入价格"
        print "       count : 买入数量"
        print "示例:python %s CTRP 2016-12-15 45.23 10" % sys.argv[0]
        #sys,exit(1)

    report = StockReport('CTRP', '2016-12-15', 41.28, 17)
    ret = report.ratio_by_month()
    print ret
