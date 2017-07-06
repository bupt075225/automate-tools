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
        print ">>>>>>>>>>>>>now draw table"
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

    def _get_asset_type(self, symbol):
        '''
        从配置文件获取目前的资产类型
        '''
        if symbol in private.configs["coins"]:
            asset_type = "coin"
        elif symbol in private.configs["shares"]:
            asset_type = "share"
        else:
            raise ValueError("Unknow asset type")

        return asset_type

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
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        years_fmt = mdates.DateFormatter("%Y-%m")
        # x轴上的刻度最大为年,最小为月
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

    def draw_figure(self):
        '''
        生成数据的曲线图
        '''
        assert isinstance(self.src_data, list)

        subplot_describle = private.configs["visual_plot"]
        subplot_amount = len(subplot_describle)

        # 创建多个子图,子图分行列放置
        fig, axs = plt.subplots(len(self.src_data), 
            subplot_amount, sharex=True)
        fig.subplots_adjust(left=0.08, right=0.98, wspace=0.3)

        labels = {}
        for index,items in enumerate(self.src_data):
            i = 0
            for i, describle in enumerate(subplot_describle):
                ax = axs[index, i]

                x_data = np.array([item["date"] for item in items],
                    dtype='datetime64').astype(datetime.datetime)
                if describle=="price curve":
                    y_data = np.array([float(item["price"]) for item in items])
                elif describle=="growth rate curve":
                    y_data = np.array([item["growth_rate_monthly"] for item in items])
                else:
                    raise ValueError("Unknow plot describle")

                ax.plot(x_data, y_data)

                self._set_subplot(ax)
                asset_type = self._get_asset_type(items[0]["symbol"])

                # 设置标题
                ax.set_title("%s %s" % (asset_type, describle))

                datemin = datetime.date(x_data.min().year, 1, 1)
                datemax = datetime.date(x_data.max().year+1, 1, 1)
                ax.set_xlim(datemin, datemax)

                labels[items[0]["symbol"]] = [x_data[-1],y_data[-1]]

                i += 1

        for k,v in labels.iteritems():
            print v
            print k
            plt.text(v[0],v[1],k,fontsize=8)

        fig.autofmt_xdate()
        # 设置子图之间的间隔
        plt.subplots_adjust(hspace=0.2)
        #plt.subplots_adjust(hspace=.0)

        filename = 'trend' + datetime.date.today().strftime('%Y%m%d') + '.png'
        plt.savefig(filename)
        return filename
