import streamlit as st


def header_view():
    # タイトル
    st.title("LogMystic")

    # 概要
    st.markdown('''
    **以下OSSのアクセスログを解析できます。**
    * Apache
    * Nginx
    ''')
