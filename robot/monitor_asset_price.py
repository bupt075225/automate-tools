#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append("/home/data/git/automate-tools/data_source")
from data_source import CoindeskDataSource

class BitcoinPriceMonitor(object):
    '''
    监视BTC价格,上涨或下跌超过阀值就发送短信
    Args:
    base: 初始价格，作为监视价格比较的初始基准
    threshold: 价格上涨或下跌阀值,超过阀值就发送短信
    '''
    def __init__(self, base, threshold):
        self.base_point = base
        self.threshold = threshold

    def _get_cur_price(self):
        data_source = CoindeskDataSource()
        cur_price = data_source.get_realtime_btc()
        return cur_price

    def compare_price(self):
        pass

if __name__=="__main__":
    monitor = BitcoinPriceMonitor(12000, 0.1)
    print monitor._get_cur_price()
