# pip install plotly

import ccxt
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


def main():
    exchange = ccxt.binance()

    data = exchange.fetch_ohlcv(
    symbol = 'BTC/USDT', timeframe = '15m', limit = 1000
    )
    header = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(data, columns = header)
    df.insert(1, 'datetime', [datetime.fromtimestamp(d/1000) for d in df.timestamp])

    fig = go.Figure(data = [
    go.Candlestick(
    x = df['datetime'],
    open = df['open'],
    high = df['high'],
    low = df['low'],
    close = df['close']
    )
    ])

    fig.show()


if __name__ == '__main__':
    main()
