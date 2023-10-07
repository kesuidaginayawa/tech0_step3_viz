import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.express as px

#<import>-------------------------------------------
# 物件データ
df = pd.read_csv('.\\distinct_mean_values.csv')
# 行政区域データ
with open(".\\town.geojson", encoding='utf-8') as f:
    twn = json.load(f)
# 駅の緯度経度データ
sttn = pd.read_csv('.\\df_stations.csv')
#---------------------------------------------------



#<fig1>---------------------------------------------
"""
# 区・町村別
"""
col1_left, col1_right = st.columns(2)
color_elem =  col1_left.selectbox('１番気になる情報',("賃料（万円）","専有面積(m^2)","件数","徒歩分数(分)"))
hover_data = col1_right.multiselect('他に気になる情報',("専有面積(m^2)","賃料（万円）","件数","徒歩分数(分)"))
# hover_data2 = st.selectbox('１番気になる情報',("件数","賃料（万円）","件数","徒歩分数(分)"))

st.subheader("平均{}".format(color_elem))
fig1 = px.choropleth_mapbox(
    df,
    geojson=twn,
    locations="所在地_市区町村",
    color=color_elem,
    hover_name="所在地_市区町村",
    hover_data=hover_data,
    featureidkey="properties.N03_004",
    mapbox_style="carto-positron",
    zoom=10,
    center={"lat":35.45, "lon": 139.58},
    opacity=0.5,
    width=800,
    height=800,
)
fig1.update_layout(
    autosize=True,
    # width=700,  # Width in pixels
    # height=700,  # Height in pixels
)
st.plotly_chart(fig1, use_container_width=True)
#--------------------------------------------------

#<fig2>---------------------------------------------
"""
# 駅別
"""

towns = sttn['所在地_市区町村'].unique().tolist()

col2_left, col2_right = st.columns(2)
town = col2_left.selectbox('気になる町',(towns))
color = col2_right.selectbox('気になる情報',("賃料（万円）","専有面積(m^2)"))

t_sttn = sttn[sttn['所在地_市区町村']==town]
fig2 = px.scatter_mapbox(
    t_sttn, 
    lat="lat", 
    lon="lon", 
    color=color, 
    size="件数",
    size_max=40, 
    zoom=13,
    mapbox_style="carto-positron",
    hover_data=["沿線", "駅"]
    )

fig2.update_layout(
    autosize=True,
    width=700,  # Width in pixels
    height=700,  # Height in pixels
)

st.plotly_chart(fig2, use_container_width=True)

#--------------------------------------------------