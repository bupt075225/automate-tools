# -*- coding:utf-8 -*-

import json
import datetime

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import private
from utils import get_date_monthly

class InvestmentVisual(object):
    '''
    输入一组或多组数据,绘制各自表图
    '''
    def __init__(self, src_data):
        self.src_data = src_data

    def _data_analysis(self, data):
        '''
        源数据转为JSON格式作为pandas输入,
        以HTML形式输出pandas数据表格
        '''
        src = json.dumps(data)
        df = pd.read_json(src)
        return df

    def draw_table(self):
        '''
        生成数据表格,以HTML格式输出
        '''
        assert isinstance(self.src_data, list)
        style = "<style>td {  text-align: center;  padding: 5px;}" \
            "  thead {  align: left;  background-color: #a7a37e;}" \
            "  tfoot tr:nth-child(odd) {   background-color: #efecca; }" \
            "  tbody tr:nth-child(even) {   background-color: #efecca; }  </style>"
        table_html = ""
        table_html += style
        for data in self.src_data:
            data_frame = self._data_analysis(data)
            table_html += data_frame.to_html(border=0)
            table_html += "<br>"

        return table_html

    def _set_subplot(self, ax):
        '''
        设置子图通用的样式
        '''

        ax.grid(True)

        # 不显示子图上面和右面的边框线
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # 只显示左边纵轴和下方横轴上的刻度
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        
        # 使用日期年月来描横轴上的点
        months = mdates.MonthLocator()
        years_fmt = mdates.DateFormatter("%Y-%m")
        # x轴上的刻度为年
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(years_fmt)

        # 设置坐标轴上刻度字体大小,旋转日期,否则会挤在一起
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_rotation(40)
            tick.label.set_ha("right")

        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(10)

    def draw_figure(self):
        '''
        生成数据的曲线图
        '''
        assert isinstance(self.src_data, list)

        fig, axes = plt.subplots(1, 1)
        self._set_subplot(axes)

        date_list = get_date_monthly("2016-12-15")
        x_tick = np.array(date_list,
            dtype='datetime64').astype(datetime.datetime)

        # 设置X轴上显示的日期间隔
        if len(date_list) > 6:
            axes.xaxis.set_ticks(x_tick[::2])

        # 设置标题
        axes.set_title("Compound growth rate")
        plt.ylabel("percentage", fontsize=12)

        for index,items in enumerate(self.src_data):
            date_list = [item["date"] for item in items]
            x = np.array(date_list,
                    dtype='datetime64').astype(datetime.datetime)
            y = np.array([item["growth_rate_monthly"]*100 for item in items])
            # 描点画线
            axes.plot(x, y)

            axes.text(x[-1],y[-1],items[0]["symbol"],fontsize=12)

        filename = 'trend' + datetime.date.today().strftime('%Y%m%d') + '.png'
        plt.savefig(filename)
        return filename
