import ccxt
import pandas as pd
from datetime import datetime
import time

exchange = ccxt.bitstamp({
    'enableRateLimit':True,
    })

msec = 1000
minute = 60*msec
hour = 60 * minute
now = exchange.milliseconds()

def get_candles(symbol, timeframe, limit, from_timestamp,):

    try:
        candles = exchange.fetch_ohlcv(
            symbol = symbol,
            timeframe = timeframe,
            limit = limit,
            since = from_timestamp,
        )

        header = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(candles, columns = header)
        df.insert(1, 'datetime',  [datetime.fromtimestamp(d/1000) for d in df.timestamp])
        return df.sort_values(by='timestamp', ascending = False)


    except Exception as e:
        print('No more data')
        pass

def save_candles(symbol, timeframe, limit, from_timestamp):

    while(from_timestamp < now):
        candles = get_candles(symbol, timeframe, limit, from_timestamp)
        if len(candles) > 0:
            from_timestamp = int(candles['timestamp'].iloc[0] + minute)
        else:
            from_timestamp += hour * 1000
            pass

        print(candles)


save_candles(
symbol = 'BTC/USDT',
timeframe = '1h',
limit = 1500,
from_timestamp = exchange.parse8601('2018-01-01 00:00:00')
)
