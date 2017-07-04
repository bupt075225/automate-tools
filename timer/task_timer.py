#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
定时执行任务的定时触发模块
'''

import datetime
import time
from dateutil.relativedelta import relativedelta
import sched
import sys
import subprocess

sys.path.append('/home/data/git/automate-tools/financeBot')
from investment_report import StockReport
from sendEmail import email
from visual import InvestmentVisual
import private


scheduler = sched.scheduler(time.time, time.sleep)

class timer(object):
    '''
    通过python内置模块sched实现的定时器,定时器触发
    后,由任务执行函数重新调试下次继续执行的任务
    '''
    def __init__(self, tasks):
        self.tasks = tasks

    def trigger(self):
        for task in self.tasks:
            scheduler.enter(task['delay'], 0, task['action'], task['args'])
        scheduler.run()

class task(object):
    '''
    任务基类,所有定制任务都是它的子类,提供重新调度任务的
    方法供所有子任务使用,还提供计算当前时该到用户设定时间的
    间隔的方法,以秒为单位
    提供周期为天或月的定时任务
    '''
    def __init__(self, datetime="25 12:15", hour=None, args=()):
        self.arguments = args
        self.datetime = datetime  #每月执行日期,格式:"25 12:15"
        self.hour = hour          #每天执行时间,格式:"15:44"
        self.timeDelta = self.calculate_time_delta()

    def reschedule(self, action, argument, delay_time):
        scheduler.enter(delay_time, 0, action, argument)

    def calculate_time_delta(self):
        if self.hour != None:
            '''
            每天定时执行的任务时间间隔
            '''
            now = datetime.datetime.now()
            print "Now time: %s" % now
            timeStr = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + self.hour
            future = datetime.datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
            print "Task running time: %s" % future
            if future <= now:
                future = future + relativedelta(days=+1)
                print "Lost today and next time is %s" % future
        else:
            '''
            每月定时执行的任务时间间隔
            '''
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

class StockTask(task):
    '''
    定时运行的股票信息报告任务
    '''
    def __init__(self, datetime="25 12:15", hour=None, args=()):
        super(StockTask, self).__init__(datetime, hour, args)

    def run_stock_task(self):
        delay_time = self.calculate_time_delta()
        self.reschedule(self.run_stock_task, self.arguments, delay_time)
        print "I am working in stock task"
        reports = []
        # 生成每支股票的报告内容
        for stock in private.configs['stocks']:
            report = StockReport(stock['symbol'], stock['date'], 
                                 stock['buyPrice'], stock['count'])
            ret = report.ratio_by_month()
            reports.append(ret)

        abstract = ""
        data_detail = []
        # 报告转为邮件内容
        for ret in reports:
            assert isinstance(ret['detail'], list)
            abstract += '<p>%s total growth rate: %s</p>' % (ret['symbol'], ret['growth_rate'])
            data_detail.append(ret["detail"])

        v = InvestmentVisual(data_detail)
        tables = '<p>%s</p>' % (v.draw_table())
        print ">>>>>>now to draw"
        image_name = v.draw_figure()

        email_content = {}
        email_content['toAddr'] = private.configs['notify_email']
        email_content['subject'] = '投资报告'
        email_content['content'] = abstract.encode('utf-8') + tables.encode('utf-8')
        email_content['image_name'] = image_name 
        mail = email()
        msg = mail.writeEmail(**email_content)
        mail.sendEmail(email_content['toAddr'], msg)

class RestartWebSiteTask(task):
    '''
    每天重启一次xilingxue网站,暂时规避运行一段时间后
    数据库连接句柄失效的问题
    '''
    def __init__(self, datetime=None, hour="2:30", args=()):
        super(RestartWebSiteTask, self).__init__(datetime, hour, args)

    def run_restart_site_task(self):
        delay_time = self.calculate_time_delta()
        self.reschedule(self.run_restart_site_task, self.arguments, delay_time)
        subprocess.Popen("supervisorctl restart xilingxue", shell=True)


if __name__=="__main__":
    restart_web_task = RestartWebSiteTask(hour="2:30")
    send_report_task = StockTask(datetime="5 6:49")
    tasks = [
        {'delay':restart_web_task.timeDelta, 'action':restart_web_task.run_restart_site_task, 'args':tuple()},
        {'delay':send_report_task.timeDelta, 'action':send_report_task.run_stock_task, 'args':tuple()},
    ]
    testTimer = timer(tasks)
    testTimer.trigger()

