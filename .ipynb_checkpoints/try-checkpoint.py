import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf

start = '2016-01-01'
end = dt.datetime.now()
stock_code = '^GSPC'
df = yf.download(stock_code, start, end, interval='1d')
# print(df.head(65))

fig, ax = mpf.plot(df[50:100],type='candle',volume=True,mav=(5,25),figratio=(12,8))
legend = ['Short_SMA', 'Long_SMA']
ax[0].legend(legend,fontsize=16)