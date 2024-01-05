import user_agents
import streamlit as st
import pandas as pd
import re
import requests
import matplotlib.pyplot as plt
import sys
import pydeck as pdk

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

# ファイルアップローダー
# Streamlitでファイルをアップロードするウィジェットを作成
uploaded_file = st.file_uploader("ログファイルをアップロードしてください", type="txt")

if uploaded_file is not None:
    # ファイルの内容を読み込む
    data = uploaded_file.read().decode("utf-8").splitlines()

    progress_text = "ログ解析 進捗状況"
    progress_bar = st.progress(0, text=progress_text)
    # 正規表現パターン
    if genre == 'Apache' or 'Nginx':
        pattern = re.compile(
            r'(\S+) - - \[(.*?)\] "(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (.+?) HTTP/1\.[01]" (\d+) (\d+) "(.*?)" "(.*?)"(?: (\S+))?$'
        )

        # データの解析
        parsed_data = [pattern.match(line).groups()
                       for line in data if pattern.match(line)]

        # DataFrameの作成
        df = pd.DataFrame(parsed_data, columns=[
            'IP', 'Datetime', 'Method', 'Path', 'Status', 'Size', 'Referrer', 'User-Agent', 'ResponseTime'
        ])

        # Datetime列をdatetime型に変換
        df['Datetime'] = pd.to_datetime(
            df['Datetime'], format='%d/%b/%Y:%H:%M:%S %z')

        # Size列とResponseTime列を数値型に変換
        df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
        df['ResponseTime'] = pd.to_numeric(df['ResponseTime'], errors='coerce')

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

        if 'ResponseTime' in df.columns and df['ResponseTime'].notnull().any():
            average_response_time = df['ResponseTime'].mean()
            median_response_time = df['ResponseTime'].median()
            min_response_time = df['ResponseTime'].min()
            max_response_time = df['ResponseTime'].max()

            # 結果の表示
            st.text(f'応答時間の平均: {average_response_time:.3f} 秒')
            st.text(f'応答時間の中央値: {median_response_time:.3f} 秒')
            st.text(f'応答時間の最小: {min_response_time:.3f} 秒')
            st.text(f'応答時間の最大: {max_response_time:.3f} 秒')
        else:
            st.text('応答時間のデータが含まれていません。')

    progress_bar.progress(10)
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

    progress_bar.progress(20)
    # ユーザーエージェントの解析

    def parse_user_agent(ua_string):
        ua = user_agents.parse(ua_string)
        os_family = ua.os.family
        browser_family = ua.browser.family
        return pd.Series([os_family, browser_family])

    df[['OS', 'Browser']] = df['User-Agent'].apply(parse_user_agent)

    progress_bar.progress(30)
    # OS の分布
    st.text('OS の分布')
    os_distribution = df['OS'].value_counts()
    st.write(os_distribution)

    # OS の円グラフ
    fig, ax = plt.subplots()
    ax.pie(os_distribution.values, labels=os_distribution.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

    progress_bar.progress(40)
    # ブラウザの分布
    st.text('ブラウザの分布')
    browser_distribution = df['Browser'].value_counts()
    st.write(browser_distribution)

    # ブラウザの円グラフ
    fig, ax = plt.subplots()
    ax.pie(browser_distribution.values,
           labels=browser_distribution.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

    progress_bar.progress(60)
    # IPアドレスのカウント
    ip_counts = df['IP'].value_counts().reset_index()
    ip_counts.columns = ['IP', 'Count']

    # 上位N件を取得（例としてトップ10）
    top_n = 10
    top_ips = ip_counts.head(top_n)

    # ジオロケーション情報を取得する関数
    def get_geolocation(ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            country = data.get('country', 'Unknown')
            city = data.get('city', 'Unknown')
            loc = data.get('loc', '')
            if loc:
                latitude, longitude = loc.split(',')
            else:
                latitude, longitude = 'Unknown', 'Unknown'
        except Exception as e:
            country, city, latitude, longitude = 'Unknown', 'Unknown', 'Unknown', 'Unknown'
        return pd.Series([country, city, latitude, longitude])

    # ジオロケーション情報の追加
    top_ips[['Country', 'City', 'Latitude', 'Longitude']
            ] = top_ips['IP'].apply(get_geolocation)

    # 結果の表示
    st.text('アクセス回数の多いクライアント一覧')
    st.write(top_ips)

    progress_bar.progress(80)
    # 緯度と経度のデータ型を float に変換
    top_ips['Latitude'] = pd.to_numeric(top_ips['Latitude'], errors='coerce')
    top_ips['Longitude'] = pd.to_numeric(top_ips['Longitude'], errors='coerce')

    # 緯度と経度のデータが存在する行のみを抽出
    top_ips_clean = top_ips.dropna(subset=['Latitude', 'Longitude'])

    # 列名の変更
    top_ips_clean = top_ips_clean.rename(
        columns={'Latitude': 'latitude', 'Longitude': 'longitude'})

    # サイズ列の追加（アクセス回数をサイズに使用）
    top_ips_clean['size'] = top_ips_clean['Count']

    # カラーコードの作成（国ごとに色分け）
    import matplotlib.cm as cm
    import matplotlib.colors as colors

    # 国名をカテゴリカルデータに変換し、整数の色コードにマッピング
    top_ips_clean['color_code'] = top_ips_clean['Country'].astype(
        'category').cat.codes

    # ユニークな国の数を取得
    num_countries = top_ips_clean['color_code'].nunique()

    # カラーマップを取得
    colormap = cm.get_cmap('tab20', num_countries)

    # color_code を RGB 値に変換
    def map_color_code_to_rgb(color_code):
        rgb = colormap(color_code)[:3]  # RGBAのうちRGBを取得
        return [int(c * 255) for c in rgb]

    top_ips_clean['color'] = top_ips_clean['color_code'].apply(
        map_color_code_to_rgb)

    # pydeck を使用して地図を表示
    import pydeck as pdk

    # レイヤーの定義
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=top_ips_clean,
        get_position='[longitude, latitude]',
        get_radius='size * 1000',  # 固定サイズに設定（適宜調整）
        get_fill_color='color',  # 赤色に固定
        pickable=True
    )

    # ビューの定義
    view_state = pdk.ViewState(
        longitude=top_ips_clean['longitude'].mean(),
        latitude=top_ips_clean['latitude'].mean(),
        zoom=1,
        pitch=0
    )

    # ツールチップの定義
    tooltip = {
        "html": "<b>IP:</b> {IP} <br/> <b>Count:</b> {Count} <br/> <b>Country:</b> {Country} <br/> <b>City:</b> {City}",
        "style": {"color": "white"}
    }

    # Deck の定義
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    # 地図の表示
    st.pydeck_chart(r)
    progress_bar.progress(100)
