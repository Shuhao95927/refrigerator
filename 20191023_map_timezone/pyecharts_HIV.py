# --*-- coding: utf8 --*--
#

import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from countries_conf import location_dict
# import matplotlib.pyplot as plt

frame_HIV = pd.read_csv("HIV_global.csv")
frame_HIV["location"] = frame_HIV["location"].apply(lambda x: location_dict.get(x, x))
frame_HIV["val"] = frame_HIV["val"].astype(np.int64)

tl = Timeline(init_opts=opts.InitOpts(width="1920px", height="900px")).add_schema(play_interval=500, is_auto_play=True)
for year in range(1990, 2018, 1):
    # 筛选对应年份的数据
    df_year = frame_HIV[frame_HIV["year"] == year]
    _stas = df_year[["location", "val"]].groupby("location").sum()

    # 清洗pyecharts绘图需要的数据
    draw_data = []
    for index, row in _stas.reset_index().iterrows():
        draw_data.append((row["location"], row["val"]))

    map0 = (
            Map(init_opts=opts.InitOpts(width="1920px", height="900px"))
            .add("HIV", draw_data, "world", is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="The Global Distribution of HIV Infections from 1990 to 2017",
                                          title_link=None,
                                          title_target=None,
                                          subtitle="By Yiqing Wang, October 2019 "
                                                   "\nData source: Global Health Data Exchange",
                                          subtitle_link="http://ghdx.healthdata.org/"),
                visualmap_opts=opts.VisualMapOpts(max_=1000000),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
    tl.add(map0, "{}".format(year))
    print("完成{}年的渲染".format(year))
tl.render("Global_Distribution_of_HIV_Infections.html")