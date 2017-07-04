# -*- coding:utf-8 -*-

import json
import datetime

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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

    def draw_figure(self):
        '''
        生成数据的曲线图
        '''
        print ">>>>>debug"
        print "come here draw"
        assert isinstance(self.src_data, list)
        # 创建一个绘图对象
        fig = plt.figure()

        rows = len(self.src_data)
        for index,items in enumerate(self.src_data):
            # 创建一个个子图,子图分行放置
            ax = fig.add_subplot(rows, 1, index+1)

            x_data = np.array([item["date"] for item in items],
                dtype='datetime64').astype(datetime.datetime)
            y_data = np.array([float(item["price"]) for item in items])
            ax.plot(x_data, y_data)
            print ">>>>>debug"
            print y_data

            # 不显示上面和右面的边框线
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            # 只显示左边纵轴和下方横轴上的刻度
            ax.yaxis.set_ticks_position("left")
            ax.xaxis.set_ticks_position("bottom")
            
            # 使用日期年月来描横轴上的点
            years = mdates.YearLocator()
            months = mdates.MonthLocator()
            years_fmt = mdates.DateFormatter("%Y-%m")
            ax.xaxis.set_major_locator(years)
            ax.xaxis.set_major_formatter(years_fmt)
            ax.xaxis.set_minor_locator(months)

            datemin = datetime.date(x_data.min().year, 1, 1)
            datemax = datetime.date(x_data.max().year+1, 1, 1)
            ax.set_xlim(datemin, datemax)
            
            ax.grid(True)

            text_position_x = x_data[-1]
            text_position_y = y_data[-1]
            plt.text(text_position_x,text_position_y,
                items[0]["symbol"],fontsize=8)

            fig.autofmt_xdate()

            # 去掉最后一个子图的最后一个刻度标值
            if index+1 == len(self.src_data):
                y_ticks = ax.yaxis.get_major_ticks()
                y_ticks[-1].label1.set_visible(False)

        # 设置子图之间的间隔
        #plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(hspace=.0)

        filename = 'trend' + datetime.date.today().strftime('%Y%m%d') + '.png'
        plt.savefig(filename)
        return filename
