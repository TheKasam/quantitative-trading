import datetime as dt
import matplotlib.pyplot as plt #make plots
from matplotlib import style #make charts look pretty
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web #getting data from yahoo fin
style.use('ggplot')


#importing data from a website and saving to csv
'''
start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)



#data frame: sorta like a spread sheet
df = web.DataReader('TSLA', 'google', start, end)
#print(df.head(6)) #.tail gives you last rows #check for stocksplit

df.to_csv('TSLA.csv') '''


#opening saved data and plotting it
'''
df = pd.read_csv('TSLA.csv',parse_dates = True, index_col=0)

df['Close'].plot() #print(df[['Open','High']].head())
plt.show()'''



'''
#data manipulation

df = pd.read_csv('TSLA.csv',parse_dates = True, index_col=0)


#new colums
df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean() #100 moving average: today + previous 99days average of those. Creates that everyday
print(df.tail())
print(df.head())
                        #size #starting
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])'''

#ex 4
df = pd.read_csv('TSLA.csv',parse_dates = True, index_col=0)
start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)
df = web.DataReader('TSLA', 'yahoo', start, end)
df.to_csv('TSLA.csv')
#new data frame                #10 days #open high low close
df_ohlc = df['Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

#puts date back into colum
df_ohlc.reset_index(inplace = True)

#converting to mdates
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.xaxis_date()


candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values,0)
plt.show()
