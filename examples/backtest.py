import pybacktest
import numpy as np
import pandas as pd
import datetime as dt

e = pd.read_csv("/home/bbc/eu-ats/data/aud.csv", dtype={'Time':object})
e.Time=e.Time.apply(lambda x: x[:-6])
e.Time = pd.to_datetime(e.Time, format='%Y-%m-%d %H:%M:%S:%f')
#data = data[data['Bid']>0.1]
#e = data.set_index(pd.to_datetime(data['Time']))
#e = e.drop('Time',1)
#e = e.drop('Ask',1)
#e = e.drop('AskVolume',1)
#e = e.drop('BidVolume',1)

#e.to_csv("aud2.csv",float_format='%.5f', date_format='%Y-%m-%d %H:%M:%S:%f')
#e = pd.read_csv("aud2.csv")


x = range(len(e.Bid))
y = [i/100 for i in x]
e['n'] = y
e = e.set_index('Time')

o=e.groupby('n').head(1)
#sindex = o.index.levels[0]
tindex = o.index.levels[1]
o=o.set_index('n')
o.rename(columns={'Bid':'O'}, inplace=True)

h=e.groupby('n').aggregate(np.max)
h.rename(columns={'Bid':'H'}, inplace=True)
l=e.groupby('n').aggregate(np.min)
l.rename(columns={'Bid':'L'}, inplace=True)
c=e.groupby('n').tail(1)
c=c.set_index('n')
c.rename(columns={'Bid':'C'}, inplace=True)

ohlc = o.join(h).join(l).join(c)
ohlc = ohlc.set_index(tindex)
ohlc.index.name = 'Date'

ohlc = ohlc*100000

"""
fast, slow = 5, 10
ms = pd.rolling_mean(ohlc.C, fast)
ml = pd.rolling_mean(ohlc.C, slow)
buy = cover = (ms > ml) & (ms.shift() < ml.shift())
sell = short = (ms < ml) & (ms.shift() > ml.shift())
bt = pybacktest.Backtest(locals(), 'ma_cross')
bt.summary()
"""

def strat(ohlc, **args):
	print args
	fast, slow = args['fast'], args['slow']
	print fast, slow
	ms = pd.rolling_mean(ohlc.C, fast)
	ml = pd.rolling_mean(ohlc.C, slow)
	buy = cover = (ms > ml) & (ms.shift() < ml.shift())
	sell = short = (ms < ml) & (ms.shift() > ml.shift())
	bt = pybacktest.Backtest(locals(), 'ma_cross')
	return bt

op = pybacktest.Optimizer(strat, ohlc, processes=1)

op.add_param('fast', 5, 20, 1)
op.add_param('slow', 25, 50, 1)
r = op.results()
print r
