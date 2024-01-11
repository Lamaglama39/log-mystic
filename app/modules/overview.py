import streamlit as st


def overview(df):
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
