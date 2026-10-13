import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="多标的股票监控工作台")
st.title("📊 多股票并行监控工作台（10标的）")
st.caption("学术项目｜模拟行情演示，仅可视化，不提供自动交易功能")

watch_list = {
    "600036": "招商银行",
    "600519": "贵州茅台",
    "000001": "平安银行",
    "002594": "比亚迪",
    "601318": "中国平安",
    "000858": "五粮液",
    "600989": "宝丰能源",
    "002714": "牧原股份",
    "601899": "紫金矿业",
    "300750": "宁德时代"
}
stock_codes = list(watch_list.keys())

with st.sidebar:
    st.header("⚙️ 参数控制面板")
    period = st.radio("行情周期", ["日线", "周线"], horizontal=True)
    alert_threshold = st.slider("振幅告警阈值 %", min_value=1.0, max_value=10.0, value=3.0, step=0.2)
    fetch_count = st.slider("K线数量", min_value=20, max_value=120, value=60)
    refresh_btn = st.button("🔄 刷新全部行情")

def get_sim_data(count):
    np.random.seed(None)
    base_price = np.random.uniform(20, 200)
    price_series = base_price + np.cumsum(np.random.randn(count)*2.2)
    df = pd.DataFrame({"收盘": price_series})
    df["最高"] = df["收盘"] + np.random.uniform(0.5,3,count)
    df["最低"] = df["收盘"] - np.random.uniform(0.5,3,count)
    return df

st.subheader("标的监控列表")
for code in stock_codes:
    stock_name = watch_list[code]
    df = get_sim_data(fetch_count)

    last_price = df["收盘"].iloc[-1]
    first_price = df["收盘"].iloc[0]
    change_pct = (last_price - first_price) / first_price * 100
    high = df["最高"].max()
    low = df["最低"].min()
    amplitude = (high - low) / low * 100

    if amplitude >= alert_threshold:
        status_text = "⚠️ 异动预警"
        bg_color = "#fff2cc"
    else:
        status_text = "✅ 正常"
        bg_color = "#f0f8f0"

    fig = px.line(df, y="收盘", height=80, width=240)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_visible=False,
        yaxis_visible=False,
        showlegend=False
    )

    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 1, 1])
        with col1:
            st.write(f"**{stock_name}**\n`{code}`")
        with col2:
            st.write(f"现价：{last_price:.2f}")
        with col3:
            st.plotly_chart(fig, config={"displayModeBar": False})
        with col4:
            st.write(f"区间涨跌：{change_pct:.2f}%")
        with col5:
            st.markdown(f":{bg_color}[{status_text}]\n振幅:{amplitude:.2f}%")

st.divider()
st.info("💡 演示版本：波动超过阈值自动黄色预警，用于项目可视化展示。")
