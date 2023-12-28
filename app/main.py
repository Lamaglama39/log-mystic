import user_agents
import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import sys

# set conig
st.set_page_config(
    page_title="LogMystic",
    page_icon="❓",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Lamaglama39/log-mystic',
        'Report a bug': 'https://github.com/Lamaglama39/log-mystic',
        'About': "Log Search app!"
    }
)

# タイトル
st.title("LogMystic")

# 概要
st.markdown('''
**以下OSSのアクセスログを解析できます。**
* Apache
* Nginx
''')

# ファイル種別選択
genre = st.radio(
    "ファイル種別を選択してください",
    ["Apache", "Nginx"],
)

# st.write("You selected:", genre)

# ファイルアップローダー
# Streamlitでファイルをアップロードするウィジェットを作成
uploaded_file = st.file_uploader("ログファイルをアップロードしてください", type="txt")

if uploaded_file is not None:
    # ファイルの内容を読み込む
    data = uploaded_file.read().decode("utf-8").splitlines()

    # 正規表現パターン
    st.write(genre)
    if genre == 'Apache' or 'Nginx':
        pattern = re.compile(
            r'(\S+) - - \[(\d+/[A-Za-z]+/\d+:\d+:\d+:\d+ \+\d+)\] "(GET|POST) (.+?) HTTP/1.1" (\d+) (\d+) "(.*?)" "(.*?)"')

        # データの解析
        parsed_data = [pattern.match(line).groups()
                       for line in data if pattern.match(line)]

        # DataFrameの作成
        df = pd.DataFrame(parsed_data, columns=[
            'IP', 'Datetime', 'Method', 'Path', 'Status', 'Size', 'Referrer', 'User-Agent'])

        # Datetime列をdatetime型に変換
        df['Datetime'] = pd.to_datetime(
            df['Datetime'], format='%d/%b/%Y:%H:%M:%S %z')

        # DataFrameの表示
        st.text('先頭10行の抜粋')
        st.write(df.head(10))

        # ログ総数
        st.text(f'アクセスログ総数: {len(df)}')

        # ログ時間
        min_time = df['Datetime'].min()
        max_time = df['Datetime'].max()
        st.text(
            f'アクセスログ記録時間: {min_time} ~ {max_time}')

    # 平均リクエスト件数/分の計算
        duration_in_minutes = (max_time - min_time).total_seconds() / 60
        average_requests_per_minute = round(len(df) / duration_in_minutes, 2)
        st.text(
            f'平均リクエスト件数/分: {average_requests_per_minute} 件 / 分')

    # ステータスコード 一覧
    st.text('ステータスコードの分布')
    status_distribution = df['Status'].value_counts()
    st.write(status_distribution)

    # 円グラフの作成
    fig, ax = plt.subplots()
    ax.pie(status_distribution.values,
           labels=status_distribution.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)
