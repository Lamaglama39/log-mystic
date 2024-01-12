import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ステータスコードを数値型に変換
def num_conversion(df):
    df['Status'] = pd.to_numeric(df['Status'], errors='coerce')
    # 日時を1分単位に丸める
    df['Time'] = df['Datetime'].dt.floor('T')
    return df


# 負荷状況の線グラフ
def load_status(df):
    requests_per_time = df.groupby('Time').size().reset_index(name='Requests')

    # グラフの作成
    st.text('負荷状況（時間ごとのリクエスト数）')
    fig, ax = plt.subplots()
    ax.plot(requests_per_time['Time'], requests_per_time['Requests'])
    ax.set_xlabel('time')
    ax.set_ylabel('request count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


# エラー発生状況の線グラフ
def error_status(df):
    df['Error'] = df['Status'].between(400, 599)

    # 時間ごとのエラー数を集計
    errors_per_time = df[df['Error']].groupby(
        'Time').size().reset_index(name='Errors')

    # グラフの作成
    st.text('エラー発生状況（時間ごとのエラー数）')
    fig, ax = plt.subplots()
    ax.plot(errors_per_time['Time'], errors_per_time['Errors'])
    ax.set_xlabel('time')
    ax.set_ylabel('error count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


# クライアントエラー発生状況 (4XX) の線グラフ
def client_error_status(df):
    df['ClientError'] = df['Status'].between(400, 499)

    # 時間ごとの4XXエラー数を集計
    client_errors_per_time = df[df['ClientError']].groupby(
        'Time').size().reset_index(name='ClientErrors')

    # グラフの作成
    st.text('クライアントエラー発生状況（時間ごとの4XXエラー数）')
    fig, ax = plt.subplots()
    ax.plot(client_errors_per_time['Time'],
            client_errors_per_time['ClientErrors'])
    ax.set_xlabel('time')
    ax.set_ylabel('4XX error count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


# サーバエラー発生状況 (5XX) の線グラフ
def server_error_status(df):
    df['ServerError'] = df['Status'].between(500, 599)

    # 時間ごとの5XXエラー数を集計
    server_errors_per_time = df[df['ServerError']].groupby(
        'Time').size().reset_index(name='ServerErrors')

    # グラフの作成
    st.text('サーバエラー発生状況（時間ごとの5XXエラー数）')
    fig, ax = plt.subplots()
    ax.plot(server_errors_per_time['Time'],
            server_errors_per_time['ServerErrors'])
    ax.set_xlabel('time')
    ax.set_ylabel('5XX error count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
