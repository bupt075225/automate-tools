# -*- coding:utf-8 -*-

from __future__ import division
import time
import sys
sys.path.append("/home/data/git/data_source")
from data_source import CoindeskDataSource
from data_source import IEXDataSource
from data_source import OKCoinDataSource
from send_sms import SmsSender
from private import configs

class AssetPriceMonitor(object):
    '''
    监视资产价格,上涨或下跌超过阀值就发送短信

    参数:
    name: 资产名称,通常是股票代码
    base: 初始价格，作为价格比较的初始基准
    threshold: 价格上涨或下跌阀值,超过阀值就发送短信
    '''
    def __init__(self, name, base, threshold):
        self.asset_name = name
        self.base_price = base
        self.threshold = threshold

    def _get_cur_btc_price(self):
        data_source = CoindeskDataSource()
        try:
            cur_price = data_source.get_realtime_btc()
        except:
            print "Get digital currency price failed"
            return 0
        return cur_price

    def _get_cur_bch_price(self):
        data_source = OKCoinDataSource()
        try:
            cur_price = data_source.get_realtime_bch()
        except:
            print "Get digital currency price failed"
            return 0
        return cur_price

    def _get_cur_stock_price(self):
        data_source = IEXDataSource(self.asset_name)
        try:
            rsp = data_source.get_realtime_quote()
        except:
            print "Get stock price failed"
            return 0
        return rsp["latestPrice"]

    def get_quotes(self):
        '''
        计算当前资产价格上涨或下迭幅度
        '''
        quotes = {}
        if self.asset_name == "BTC":
            cur_price = self._get_cur_btc_price()
        elif self.asset_name == "BCH":
            cur_price = self._get_cur_bch_price()
        else:
            cur_price = self._get_cur_stock_price()

        if 0 == cur_price:
            return quotes

        delta = abs(float(cur_price) - float(self.base_price))
        percent = round(delta / self.base_price * 100, 2)
        quotes["asset_name"] = self.asset_name
        quotes["cur_price"] = cur_price
        quotes["threshold"] = self.threshold
        if cur_price < self.base_price and percent >= self.threshold:
            quotes["state"] = "下跌"
        elif cur_price > self.base_price and percent >= self.threshold:
            quotes["state"] = "上涨"
        else:
            quotes = {}

        return quotes

def check_asset_quotes(name, base, threshold):
    ret = {}
    ret["name"] = name
    ret["base"] = base
    ret["threshold"] = threshold
    monitor = AssetPriceMonitor(name, base, threshold)
    quote = monitor.get_quotes()
    if "state" in quote:
        '''
        资产状态超过阀值,更新价格比较基准
        '''
        ret["base"] = quote["cur_price"]
        print "%s asset state change" % name
        print quote
        # 发送告警短信
        params = []
        # 追加元素到list中的顺序不能变,与短信模板中的参数顺序保持一致
        params.append(quote["asset_name"])
        params.append(quote["cur_price"])
        params.append(quote["state"])
        params.append(str(quote["threshold"]) + "%")
        # 30秒内发送短信不能超过1条
        time.sleep(35)
        sender = SmsSender(configs["sms"]["appid"], configs["sms"]["appkey"])
        sender.send_with_param(configs["sms"]["phone_numbers"], 
                               configs["sms"]["templ_id"], 
                               params, 
                               configs["sms"]["sms_sign"])
    else:
        print "Check %s quotes nothing" % name

    return ret

