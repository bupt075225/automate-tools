#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
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
        return response.json()["data"]

if __name__=="__main__":
    q = IntrinioQuery("CTRP", "2016-12-12", "2017-05-12")
    ret = q.execute()
    print ret
