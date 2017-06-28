#!/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import division
import sys
import time
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from data_source import IntrinioQuery
from db import Share

class StockReport(object):
    '''
    股票盈亏报告
    '''
    def __init__(self, symbol, buy_date, price, count):
        self.symbol = symbol
        self.buy_date = buy_date
        self.buyPrice = price
        self.count = count
        self.historicalData = self._getStockInfo(self.symbol)

    def _profitRatio(self, data):
        '''
        计算每月收益率
        '''
        lastAsset = float(data['lastPrice']) * data['number']
        latestAsset = float(data['latestPrice']) * data['number']
        lastAsset = round(lastAsset,2)
        latestAsset = round(latestAsset,2)

        percent = ((latestAsset - lastAsset) / lastAsset) * 100
        return (str(round(percent, 2)) + '%')

    def _getStockInfo(self, symbol):
        #从本地数据库获取股票历史价格
        cur_date = time.strftime("%Y-%m-%d" ,time.localtime())
        data_set = Share(symbol)
        return data_set.get_historical(self.buy_date, cur_date)

        '''
        # 从intrinio获取股票历史价格
        cur_date = time.strftime("%Y-%m-%d" ,time.localtime())
        query = IntrinioQuery(symbol, self.buy_date, cur_date)
        return query.execute()
        '''

    def _getTimePoints(self, start, end=time.strftime("%Y-%m-%d" ,time.localtime())):
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
        
    def getStatistic(self):
        '''
        每月在买入日期查询一次股价,作为当月统计数据
        '''
        dataSet = self._getTimePoints(self.buy_date)

        historicalDict = {}
        for item in self.historicalData:
            historicalDict[item['date']] = item

        print self.historicalData
        print historicalDict
        print dataSet
        for data in dataSet:
            while 1:
                # 统计日期是休市日往后查,找到休市后的第一个交易日
                if not historicalDict.has_key(data['date']):
                    splitDate = data['date'].split('-')
                    next_day = datetime.date(int(splitDate[0]),int(splitDate[1]),int(splitDate[2])) + relativedelta(days=+1)
                    data['date'] = time.strftime('%Y-%m-%d', next_day.timetuple())
                else:
                    break

            data['price'] = historicalDict[data['date']]['close']
        return dataSet

    def ratioByMonth(self):
        report = {}
        result = self.getStatistic()
        count = len(result)
        i = 0
        data = {}
        while i < (count - 1):
            j = i + 1
            data['lastPrice'] = result[i]['price']
            data['latestPrice'] = result[j]['price']
            data['number'] = self.count
            ratio = self._profitRatio(data)
            result[j]['ratio'] = ratio
            i += 1
        print 'Staticstic result:'
        print result
        report['detail']=result

        if count > 1:
            data['lastPrice'] = self.buyPrice
            data['latestPrice'] = result[-1]['price']
            data['number'] = self.count
            ratio = self._profitRatio(data)
            print 'Latest date %s ratio:' % result[-1]['date']
            print ratio
            report['growth_rate'] = ratio
            report['symbol'] = self.symbol
        else:
            report['info'] = 'There is only the first month statistic data found'

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
    ret = report.ratioByMonth()
    print ret
