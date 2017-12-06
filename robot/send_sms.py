#!/usr/bin/env python
# -*- coding:utf-8 -*-

from util import SmsSenderUtil
from private import configs

class SmsSender(object):
    '''
    群发短信
    '''

    def __init__(self, appid=0, appkey=""):
        self.url = "https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2"
        self.appid = appid
        self.appkey = appkey
        self.util = SmsSenderUtil()

    def send_with_param(self, phone_numbers, templ_id, params, sign, extend="", ext=""):
        '''
        按指定模板群发短信

        Args:
            phone_numbers: 不带国家码的手机号列表
            templ_id: 模板 id
            params: 模板参数列表，如模板 {1}...{2}...{3}，那么需要带三个参数
            sign: 短信内容配置时申请的短信签名
            extend: 扩展码，可填空串
            ext: 服务端原样返回的参数，可填空串
        '''

        rnd = self.util.get_random()
        cur_time = self.util.get_cur_time()
        data = {}
        data["tel"] = self.util.phone_numbers_to_list("86", phone_numbers)
        #sign字段是短信标签，如果填空串，系统会使用默认:腾讯云
        data["sign"] = sign
        data["sig"] = self.util.sign(self.appkey, rnd, cur_time, phone_numbers)
        data["tpl_id"] = templ_id
        data["params"] = params
        data["time"] = cur_time
        data["extend"] = extend
        data["ext"] = ext

        whole_url = self.url + "?sdkappid=" + str(self.appid) + "&random=" + str(rnd)
        return self.util.send_post_request("yun.tim.qq.com", whole_url, data)

if __name__ == "__main__":
    phone_numbers = configs["phone_numbers"]
    templ_id = configs["templ_id"]
    sign = configs["sms_sign"]
    params = ["BCH", "1500", "上涨", "10%"]

    sender = SmsSender(configs["appid"], configs["appkey"])
    ret = sender.send_with_param(phone_numbers, templ_id, params, sign)
    print ret
