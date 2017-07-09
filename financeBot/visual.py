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

        subplot_describle = private.configs["visual_plot"]
        subplot_type_amount = len(subplot_describle)

        # 每种类型的子图占一行,每种类型包含的子图有2个各占一列
        fig, axs = plt.subplots(subplot_type_amount, 2)
        fig.subplots_adjust(left=0.08, right=0.98, wspace=0.3)
        # 设置子图之间的间隔
        plt.subplots_adjust(hspace=0.5)

        for index,items in enumerate(self.src_data):
            i = 0
            asset_type = self._get_asset_type(items[0]["symbol"])
            if asset_type=="share":
                row_index = 0
            elif asset_type=="coin":
                row_index = 1
            else:
                raise ValueError("Unknow asset type")

            for i, describle in enumerate(subplot_describle):
                ax = axs[row_index, i]

                date_list = [item["date"] for item in items]
                x_tick = np.array(date_list,
                    dtype='datetime64').astype(datetime.datetime)
                if describle=="price curve":
                    y_tick = np.array([float(item["price"]) for item in items])
                elif describle=="growth rate curve":
                    y_tick = np.array([item["growth_rate_monthly"] for item in items])
                else:
                    raise ValueError("Unknow plot describle")

                # 描点画线
                ax.plot(x_tick, y_tick)

                self._set_subplot(ax)
                # 设置X轴上显示的日期间隔
                if len(date_list) > 6:
                    ax.xaxis.set_ticks(x_tick[::2])

                # 设置标题
                ax.set_title("%s %s" % (asset_type, describle))

                x_tick_min = datetime.date(x_tick.min().year,x_tick.min().month,1)
                x_tick_max = datetime.date(x_tick.max().year,x_tick.max().month+1,1)
                ax.set_xlim(x_tick_min, x_tick_max)

                ax.text(x_tick[-1],y_tick[-1],items[0]["symbol"],fontsize=8)

                i += 1

        filename = 'trend' + datetime.date.today().strftime('%Y%m%d') + '.png'
        plt.savefig(filename)
        return filename
