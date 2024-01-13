import matplotlib.colors as colors
import matplotlib.cm as cm
import streamlit as st
import pandas as pd
import requests
import pydeck as pdk


def geolocation(df):
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
    return top_ips


def frequently_accessed_clients(top_ips):
    # 結果の表示
    st.text('アクセス回数の多いクライアント一覧')
    st.write(top_ips)


# 地図グラフ
def client_map_graph(top_ips):
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
