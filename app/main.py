import streamlit as st

import modules.config
import modules.log_pattern
import modules.log_analysis
import modules.overview
import modules.pie_graph
import modules.line_graph
import modules.map_graph

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

    # プログレスバー
    progress_text = "ログ解析 進捗状況"
    progress_bar = st.progress(0, text=progress_text)

    # アクセスログ判別
    if genre == 'Apache' or 'Nginx':
        # アクセスログ解析
        pattern = modules.log_pattern.log_pattern()
        df = modules.log_analysis.log_analysis(pattern, data)

    # 解析概要
    modules.overview.overview(df)
    progress_bar.progress(10)

    # ステータスコードの分布
    modules.pie_graph.statuscord_graph(df)

    progress_bar.progress(20)
    # OS の分布
    modules.pie_graph.os_graph(df)

    progress_bar.progress(40)
    # ブラウザの分布
    modules.pie_graph.browser_graph(df)

    progress_bar.progress(50)

    # 棒グラフ
    status_num = modules.line_graph.num_conversion(df)

    modules.line_graph.load_status(status_num)
    progress_bar.progress(50)

    modules.line_graph.error_status(status_num)
    progress_bar.progress(50)

    modules.line_graph.client_error_status(status_num)
    progress_bar.progress(50)

    modules.line_graph.server_error_status(status_num)
    progress_bar.progress(50)

    progress_bar.progress(60)

    # アクセス数の多いクライアント
    top_ips = modules.map_graph.geolocation(df)

    modules.map_graph.frequently_accessed_clients(top_ips)
    progress_bar.progress(80)

    # クライアントを地図上にマッピング
    modules.map_graph.client_map_graph(top_ips)
    progress_bar.progress(100)
