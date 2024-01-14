import pandas as pd


def log_analysis(pattern, data):
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

    return df
