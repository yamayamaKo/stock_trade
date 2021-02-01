import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf

start = '2016-01-01'
end = dt.datetime.now()
stock_code = '^CSPC'
df = yf.download(stock_code, start, end, interval='1d')
print(df.head())
shortTerm = 20
longTerm = 60
stopLoss = 0.95
rikaku_day = 80

# chek the highest price in the past {term} times
df['Highest'+str(shortTerm)] = df.iloc[:, 5].rolling(window=shortTerm).max()
# chek the highest price in the past {term} times
df['Lowest'+str(shortTerm)] = df.iloc[:, 5].rolling(window=shortTerm).min()

# chek the highest price in the past {term} times
df['Highest'+str(longTerm)] = df.iloc[:, 5].rolling(window=longTerm).max()
# chek the highest price in the past {term} times
df['Lowest'+str(longTerm)] = df.iloc[:, 5].rolling(window=longTerm).min()

# judge U trend or Down trend by DC
buy_position = False # 1 means entered and 0 means not already entered
sell_position = False
buy_dates = 0 # 買った（売った）後に経過した日数
sell_dates = 0
buy_stopLine = 0 # 損切りライン
sell_stopLine = 0
counter = 0 
percentChange = []

for i in range(1, len(df)):

    shortHighest = df['Highest'+str(shortTerm)][i-1]
    shortLowest = df['Lowest'+str(shortTerm)][i-1]
    longHighest = df['Highest'+str(longTerm)][i-1]
    longLowest = df['Lowest'+str(longTerm)][i-1] 
    # high_price = df['High'][i]
    # low_price = df['Low'][i]
    close = df['Adj Close'][i]
    
    # avoid NaN data 
    # 買いトレンド
    if (np.isnan(longHighest)) == False:
        if (close > longHighest and buy_position == False):
            print('Up trend')
            buy_position = True
            buy_price = close
            buy_stopLine = close * stopLoss
            print('Buy at the price {}'.format(buy_price))
    
    # 売りトレンド
    if (np.isnan(longLowest)) == False:
        if (close < longLowest and sell_position == False):
            print('Down trend')
            sell_position = True
            sell_price = close
            sell_stopLine = close * stopLoss
            print('Sell at the price {}'.format(sell_price))

    # 損切り
    if buy_position == True and close < buy_price*stopLoss:
        buy_position = False
        percent = (close/buy_price - 1) * 100
        percentChange.append(percent)
    if sell_position == True and close > (sell_price + sell_price*(1-stopLoss)):
        sell_position = False
        percent = (sell_price/close - 1) * 100
        percentChange.append(percent)

    # 利確
    if buy_dates == 80:
        buy_position = False
        percent = (close/buy_price - 1) * 100
        percentChange.append(percent)
        buy_date = 0
    if sell_dates == 80:
        sell_position = False
        percent = (sell_price/close - 1) * 100
        percentChange.append(percent)

    # 損切りラインの更新
    # if buy_position = 

    #  最終日にまだ持ってたら利確する
    if (counter == df['Adj Close'].count() - 1):
        if buy_position == True:
            buy_position = False
            percent = (close / buy_price - 1) * 100
            percentChange.append(percent)
            buy_dates = 0
        if sell_position == True:
            sell_position = False
            percent = (sell_price/close - 1) * 100
            percentChange.append(percent)
            sell_dates = 0

    # 買ってからの日数を更新する
    if buy_position == True:
        buy_dates += 1
    if sell_position == True:
        sell_dates += 1
    counter += 1



print(percentChange)

# statistic
gains = 0
numGains = 0
losses = 0
numLosses = 0
total_return = 1

for i in percentChange:
    if i > 0:
        numGains += 1
        gains += i
    else:
        numLosses += 1
        losses += i
    total_return = total_return * ((i / 100) + 1)

total_return = round((total_return - 1)*100, 2)

if numGains > 0:
    average_gain = gains / numGains
    max_return = max(percentChange)
else:
    average_gain = 0
    max_return = 'unknown'
    
if numLosses > 0:
    average_loss = losses / numLosses
    max_loss = min(percentChange)
    risk_reward_retio = - average_gain / average_loss
else:
    average_loss = 0
    max_loss = 'unknown'
    risk_reward_retio = 'inf'
    
if numGains > 0 or numLosses > 0:
    batting_ratio = numGains / (numGains + numLosses)
else:
    batting_ratio = 0
    
print('The period is from {} up to {}'.format(df.index[0], df.index[-1]))
print('Trades: {}'.format(numGains+numLosses))
print('Total return: {}%'.format(total_return))
print('Average Gain: {}'.format(average_gain))
print('Average Loss: {}'.format(average_loss))
print('Max Return: {}'.format(max_return))
print('Max Loss: {}'.format(max_loss))
print('Gain/Loss Ratio: {}'.format(risk_reward_retio))
print('Batting Average: {}'.format(batting_ratio))