#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
定时执行任务的定时触发模块
'''

import datetime
import time
from dateutil.relativedelta import relativedelta
import sched
from queryStockPrice import StockReport
from sendEmail import email

scheduler = sched.scheduler(time.time, time.sleep)

class timer(object):
    '''
    通过python内置模块sched实现的定时器,定时器触发
    后,由任务执行函数重新调试下次继续执行的任务
    '''
    def __init__(self, action, arguments=(), delay=3):
        self.action = action
        self.actionArg = arguments
        self.delay = delay

    def trigger(self):
        scheduler.enter(self.delay, 0, self.action, self.actionArg)
        scheduler.run()

class task(object):
    '''
    任务基类,所有定制任务都是它的子类似,提供重新调试任务的
    方法供所有子任务使用,还提供计算当前时该到用户设定时间的
    间隔,以秒为单位
    '''
    def __init__(self, datetime="25 12:15", hour=None, args=()):
        self.arguments = args
        self.datetime = datetime  #每月执行日期,格式:"25 12:15"
        self.hour = hour          #每天执行时间,格式:"15:44"
        self.timeDelta = self.calculateTimeDelta()

    def reschedule(self, action, argument, delayTime):
        scheduler.enter(delayTime, 0, action, argument)

    def calculateTimeDelta(self):
        if self.hour != None:
            now = datetime.datetime.now()
            print "Now time: %s" % now
            timeStr = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + self.hour
            future = datetime.datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
            print "Task running time: %s" % future
            if future <= now:
                future = future + relativedelta(days=+1)
                print "Lost today and next time is %s" % future
        else:
            now = datetime.datetime.now()
            print "Now time: %s" % now
            timeStr = str(now.year) + '-' + str(now.month) + '-' + self.datetime
            future = datetime.datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
            print "Task running time: %s" % future
            if future <= now:
                future = future + relativedelta(months=+1)
                print "Lost this month and next time is %s" % future
        delta = future - now
        print "Time delta: %d" % delta.total_seconds()
        return delta.total_seconds()

class stockTask(task):
    def __init__(self, datetime="25 12:15", hour=None, args=()):
        super(stockTask, self).__init__(datetime, hour, args)

    def runStockTask(self):
        delayTime = self.calculateTimeDelta()
        self.reschedule(self.runStockTask, self.arguments, delayTime)
        print "I am working in stock task"
        report = StockReport('CTRP', '2016-12-15', 41.28, 17)
        ret = report.ratioByMonth()
        emailContent = {}
        emailContent['toAddr'] = 'nonprivatemail@163.com'
        emailContent['subject'] = '月度财务报告'
        emailContent['content'] = str(ret)
        mail = email()
        msg = mail.writeEmail(**emailContent)
        mail.sendEmail(emailContent['toAddr'], msg)

if __name__=="__main__":
    testTask = stockTask(datetime="28 12:10")
    testTimer = timer(testTask.runStockTask, delay=testTask.timeDelta)
    testTimer.trigger()

