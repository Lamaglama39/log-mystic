import user_agents
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def statuscord_graph(df):
    st.text('ステータスコードの分布')

    # ステータスコードのカウントを取得し、データフレームに変換
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['StatusCode', 'Count']

    # 全体比(%)を計算
    total_requests = len(df)
    status_counts['Percentage (%)'] = (status_counts['Count'] /
                                       total_requests * 100).round(2)

    # 2つの列を作成
    status1, status2 = st.columns(2)

    with status1:
        # 円グラフの作成
        fig, ax = plt.subplots()
        ax.pie(status_counts['Count'],
               labels=status_counts['StatusCode'], autopct='%1.1f%%')
        ax.axis('equal')  # 円を真円にする
        st.pyplot(fig)

    with status2:
        # テーブルの表示
        st.write(status_counts)


# ユーザーエージェントの解析
def os_graph(df):
    def parse_user_agent(ua_string):
        ua = user_agents.parse(ua_string)
        os_family = ua.os.family
        browser_family = ua.browser.family
        return pd.Series([os_family, browser_family])

    df[['OS', 'Browser']] = df['User-Agent'].apply(parse_user_agent)

    st.text('OS の分布')

    # OS のカウントを取得し、データフレームに変換
    os_counts = df['OS'].value_counts().reset_index()
    os_counts.columns = ['OS', 'Count']

    # 全体比(%)を計算
    total_os = os_counts['Count'].sum()
    os_counts['Percentage (%)'] = (
        os_counts['Count'] / total_os * 100).round(2)

    # 2つの列を作成
    os1, os2 = st.columns(2)

    with os1:
        # 円グラフの作成
        fig, ax = plt.subplots()
        ax.pie(os_counts['Count'], labels=os_counts['OS'], autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)

    with os2:
        # テーブルの表示
        st.write(os_counts)


def browser_graph(df):
    st.text('ブラウザの分布')
    browser_counts = df['Browser'].value_counts().reset_index()
    browser_counts.columns = ['Browser', 'Count']

    # 全体比(%)を計算
    total_browser = browser_counts['Count'].sum()
    browser_counts['Percentage (%)'] = (
        browser_counts['Count'] / total_browser * 100).round(2)

    # 2つの列を作成
    browser1, browser2 = st.columns(2)

    # ブラウザの円グラフ
    with browser1:
        fig, ax = plt.subplots()
        ax.pie(browser_counts['Count'],
               labels=browser_counts['Browser'], autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)

    with browser2:
        st.write(browser_counts)
