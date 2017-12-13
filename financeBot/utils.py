# -*- coding:utf-8 -*-

import httplib
import json
import random
import time
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
import hashlib

class SmsSenderUtil(object):
    def get_random(self):
        return random.randint(100000, 999999)
    def get_cur_time(self):
        return long(time.time())

    def phone_numbers_to_list(self, nation_code, phone_numbers):
        tel = []
        for phone_number in phone_numbers:
            tel.append({"nationcode":nation_code, "mobile":phone_number})

        return tel

    def sign(self, appkey, rnd, cur_time, phone_numbers):
        '''
        "sig"字段根据公式sha256(appkey=$appkey&random=$random&time=$time&mobile=$mobile)生成
        '''
        phone_numbers_string = phone_numbers[0]
        for i in range(1, len(phone_numbers)):
            phone_numbers_string += "," + phone_numbers[i]
        return hashlib.sha256("appkey=" + appkey + "&random=" + str(rnd)
            + "&time=" + str(cur_time) + "&mobile=" + phone_numbers_string).hexdigest()

    def send_post_request(self, host, url, data):
        con = None

        try:
            con = httplib.HTTPSConnection(host)
            con.request('POST', url, json.dumps(data))
            response = con.getresponse()
            if '200' != str(response.status):
                obj = {}
                obj['result'] = -1
                obj['errmsg'] = "connect failed:\t" + str(response.status) + " " + response.reason
                result = json.dumps(obj)
            else:
                result = response.read()
        except Exception,e:
            obj = {}
            obj['result'] = -2
            obj['errmsg'] = "connec failed:\t" + str(e)
            result = json.dumps(obj)
        finally:
            if con:
                con.close()
        return result

def get_date_monthly(start, end=time.strftime("%Y-%m-%d" ,time.localtime())):
    start_date = time.strptime(start, "%Y-%m-%d")
    end_date = time.strptime(end, "%Y-%m-%d")
    start_date = datetime.date(start_date.tm_year,start_date.tm_mon,start_date.tm_mday)
    end_date = datetime.date(end_date.tm_year,end_date.tm_mon,end_date.tm_mday)
    date_list = rrule(freq=MONTHLY, dtstart=start_date, until=end_date)
    date_list = [time.strftime("%Y-%m-%d", date.timetuple()) for date in date_list]
    return date_list
    
