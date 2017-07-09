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

class AlphavantageDataSource(object):
    '''
    从https://www.alphavantage.co提供的数据源查询股票历史报价
    查询过去20年每个交易日,或最近100个交易日的历史报价,默认查
    过去20年的报价
    '''
    def __init__(self, symbol, full=False):
        self.symbol = symbol.upper()
        # full属性为True就查过去20年所有数据,否则只查最近100个交易日的报价
        self.full = full
        self.url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"

    def execute(self):
        api_key = private.configs["alphavantage_api_key"]
        if not self.full:
            url = self.url + "&symbol=" + self.symbol + "&apikey=" + api_key
        else:
            url = self.url + "&outputsize=full&symbol=" + self.symbol + "&apikey=" + api_key

        response = requests.get(url)
        if response.status_code != 200:
            print "Get data failed from %s" % url
            print response.text
            raise ValueError

        return response.json()

class CoindeskDataSource(object):
    '''
    从http://www.coindesk.com的API获取BTC数据
    '''
    def __init__(self):
        self.historical_btc_url = "http://api.coindesk.com/v1/bpi/historical/close.json"
        self.realtime_btc_url = "http://api.coindesk.com/v1/bpi/currentprice/CNY.json"

    def get_historical_btc(self, start, end):
        url = "%s?start=%s&end=%s" % (self.historical_btc_url,start,end)
        response = requests.get(url)
        if response.status_code != 200:
            print "Get data failed from %s" % url
            print response.text
            raise ValueError

        data = response.json()
        return data["bpi"]

    def get_realtime_btc(self):
        response = requests.get(self.realtime_btc_url)
        if response.status_code != 200:
            print "Get data failed from data source"
            raise ValueError

        data = response.json()
        return data["bpi"]["USD"]["rate_float"]
        
