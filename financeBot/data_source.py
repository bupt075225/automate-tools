#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import private

class IntrinioQuery(object):
    '''
    查询指定时间段股票历史价格
    '''
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.request_url = "https://api.intrinio.com/prices"

    def _load_payload(self):
        payload = {}
        payload["identifier"] = self.symbol
        payload["start_date"] = self.start_date
        payload["end_date"] = self.end_date

        return payload

    def execute(self):
        payload = self._load_payload()
        username = private.configs["intrinio_api_auth"]["username"]
        password = private.configs["intrinio_api_auth"]["password"]
        response = requests.get(self.request_url, params=payload, 
                                auth=(username, password))
        #return response.json()["data"]
        return response.json()

class AlphavantageQuery(object):
    '''
    从https://www.alphavantage.co提供的数据源查询股票历史报价
    查询过去20年每个交易日,或最近100个交易日的历史报价,默认查
    过去20年的报价
    '''
    def __init__(self, symbol, full=False):
        self.symbol = symbol.upper()
        # full属性为True就查过去20年所有数据,否则只查最近100个交易日的报价
        self.full = full
        self.url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'

    def execute(self):
        api_key = private.configs['alphavantage_api_key']['api_key']
        if not self.full:
            url = self.url + "&symbol=" + self.symbol + "&apikey=" + api_key
        else:
            url = self.url + "&outputsize=full&symbol=" + self.symbol + "&apikey=" + api_key

        try:
            response = requests.get(url)
        except Exception:
            raise

        return response.json()

if __name__=="__main__":
    #q = IntrinioQuery("CTRP", "2016-12-12", "2017-05-12")
    q = AlphavantageQuery(symbol="CTRP")
    ret = q.execute()
    print ret
