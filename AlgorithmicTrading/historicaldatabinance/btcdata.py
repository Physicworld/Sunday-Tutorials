import pandas as pd
import pandas_ta as TA
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('btcprice.csv')
rsi = TA.rsi(close = df['market-price'], length = 30)
moving_rsi = TA.sma(close = rsi, length = 30)

fft = np.fft.fft(moving_rsi)
fftfreq = np.fft.fftfreq(len(moving_rsi), d = len(moving_rsi))

plt.style.use('classic')
fig, ax = plt.subplots(3)

ax[0].plot(df['market-price'])
ax[1].plot(rsi)
ax[1].plot(moving_rsi)
ax[2].plot(fftfreq, fft)

plt.show()
