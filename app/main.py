import streamlit as st
import pandas as pd
import re

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

        # DataFrameの表示
        st.text('先頭10行の抜粋')
        st.write(df.head(10))

        # ステータスコードの分布
        st.text('ステータスコードの分布')
        status_distribution = df['Status'].value_counts()
        # print("Status Code Distribution:\n", status_distribution)
        status_distribution

        # ユーザーエージェントのトップ
        st.text('ユーザーエージェントの分布')
        top_user_agents = df['User-Agent'].value_counts().head(5)
        top_user_agents
        # print("Top 5 User Agents:\n", top_user_agents)
