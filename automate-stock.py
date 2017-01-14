#!/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import division
from yahoo_finance import Share
import time

def profitAndCossRatio(data):
    lastAsset = float(data['lastPrice']) * data['number']
    latestAsset = float(data['latestPrice']) * data['number']
    lastAsset = round(lastAsset,2)
    latestAsset = round(latestAsset,2)
    if lastAsset > latestAsset:
        percent = ((lastAsset - latestAsset) / lastAsset) * 100
        return ('-' + str(round(percent, 2)) + '%')
    else:
        percent = ((latestAsset - lastAsset) / lastAsset) * 100
        return (str(round(percent, 2)) + '%')

def getStockInfo():
    curTime = time.strftime("%Y-%m-%d" ,time.localtime())

    # Get stock price from yahoo finance
    ctrip = Share('CTRP')
    return ctrip.get_historical(startDate, curTime)

def getStatistic(historicalData):
    startYear = startDate.split('-')[0]
    startMonth = startDate.split('-')[1]
    day = startDate.split('-')[2]
    curTime = time.strftime("%Y-%m-%d" ,time.localtime())
    curYear = curTime.split('-')[0]
    curMonth = curTime.split('-')[1]
    dataSet = []

    years = (int(curYear) - int(startYear))
    year = int(startYear)
    while years >= 0:
        if year==int(startYear):
            month = int(startMonth)
        else:
            month = 1
        while month <= 12 and month >0:
            if year==int(startYear) and startMonth == 12:
                if len(str(month))==1:
                    date = str(year) + '-0' + str(month) + '-' +day
                else:
                    date = str(year) + str(month) + '-' +day
                dataSet.append({'date':date})
                break
            if year==int(curYear) and month > int(curMonth):
                break
            if len(str(month))==1:
                date = str(year) + '-0' + str(month) + '-' +day
            else:
                date = str(year) + '-' + str(month) + '-' + day
            dataSet.append({'date':date})
            month += 1

        years -= 1
        year += 1

    for data in dataSet:
        for item in historicalData:
            if data['date']==item['Date']:
                data['price'] = item['Close']

    return dataSet

def ratioByMonth(historicalData):
    result = getStatistic(historicalData)
    count = len(result)
    i = 0
    data = {}
    while i < (count - 1):
        j = i + 1
        data['lastPrice'] = result[i]['price']
        data['latestPrice'] = result[j]['price']
        data['number'] = buyNumber
        ratio = profitAndCossRatio(data)
        result[j]['ratio'] = ratio
        i += 1
    print result

    data['lastPrice'] = buyPrice
    data['latestPrice'] = result[-1]['price']
    data['number'] = buyNumber
    ratio = profitAndCossRatio(data)
    print ratio

startDate = '2016-12-15'
buyPrice = 41.28
buyNumber = 17

if __name__=="__main__":
    historical = getStockInfo()
    ratioByMonth(historical)
