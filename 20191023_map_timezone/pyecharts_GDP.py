# --*-- coding: utf8 --*--
#

import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
from countries_conf import countries_dict

# 导入数据，并完成数据清洗
df = pd.read_csv("GDP_global.csv", encoding="gbk")
df["Country Name"] = df["Country Name"].apply(lambda x: countries_dict.get(x, x))
years = df.columns[1:].tolist()

# 开始绘图
tl = (Timeline(init_opts=opts.InitOpts(width="1920px", height="900px"))
      .add_schema(play_interval=500, is_auto_play=True))
for year in years:
    # 筛选对应年份的数据
    data = df[["Country Name", year]].values.tolist()

    map0 = (
            Map(init_opts=opts.InitOpts(width="1920px", height="900px"))
            .add("GDP", data, "world", is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Global GDP Distribution from 1960 to 2018",
                                          title_link=None,
                                          title_target=None,
                                          subtitle="By Yiqing Wang, October 2019 "
                                                   "\nData source: World Band Data",
                                          subtitle_link="https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"),
                visualmap_opts=opts.VisualMapOpts(max_=1e12, min_=1e7),
                legend_opts=opts.LegendOpts(is_show=False),
                toolbox_opts=opts.ToolboxOpts(is_show=True)
            )
        )
    tl.add(map0, "{}".format(year))
    print("完成{}年的渲染".format(year))

tl.render("Global_GDP.html")
