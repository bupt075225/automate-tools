#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json
import datetime

class visualization(object):
    '''
    数据可视化
    '''
    def __init__(self, src):
        self.source = src
        self.dataFrame = self._dataAnalysis(self.source)

    def _dataAnalysis(self, source):
        '''
        源数据转为JSON格式作为pandas输入,
        以HTML形式输出pandas数据表格
        '''
        src = json.dumps(source)
        df = pd.read_json(src)
        return df

    def generateTable(self):
        '''
        生成数据表格,以HTML格式输出
        '''
        return self.dataFrame.to_html()

    def generateFigure(self):
        '''
        指定X轴和Y轴,生成二维图
        '''
        fig = self.dataFrame.plot(x='date',y='price')
        filename = 'trend' + datetime.date.today().strftime('%Y%m%d') + '.png'
        plt.savefig(filename)
        return filename

if __name__=='__main__':
    vis = visualization([{'date': '2016-12-15', 'price': '41.330002'}, {'date': '2017-01-13', 'price': '43.529999', 'ratio': '5.32%'}, {'date': '2017-02-15', 'price': '45.459999', 'ratio': '4.43%'}, {'date': '2017-03-15', 'price': '48.66', 'ratio': '7.04%'}])
    vis.generateFigure()
