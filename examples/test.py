import pybacktest
import numpy as np
import pandas as pd
import datetime as dt

e = pd.read_csv("/home/bbc/trading/eu-ats/data/aud-fixed.csv", dtype={'Time':object})
e.Time = pd.to_datetime(e.Time, format='%Y-%m-%d %H:%M:%S:%f')
#data = data[data['Bid']>0.1]

e = e.set_index('Time')
x = range(len(e.Bid))
y = [i/100 for i in x]
e['n'] = y

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

if True:
    fast, slow = 20, 50
    ms = pd.rolling_mean(ohlc.C, fast)
    ml = pd.rolling_mean(ohlc.C, slow)
    buy = cover = (ms > ml) & (ms.shift() < ml.shift())
    sell = short = (ms < ml) & (ms.shift() > ml.shift())
    bt = pybacktest.Backtest(locals(), 'ma_cross')
    bt.summary()

else:
    def strat(ohlc, **args):
        print args
        fast, slow = args['fast'], args['slow']
        print fast, slow
        ms = pd.rolling_mean(ohlc.C, fast)
        ml = pd.rolling_mean(ohlc.C, slow)
        buy = cover = (ms > ml) & (ms.shift() < ml.shift())
        sell = short = (ms < ml) & (ms.shift() > ml.shift())
        x={}
        x['buy']=buy
        x['cover']=cover
        x['sell']=sell
        x['short']=short
        x['ohlc']=ohlc
        for k, v in x.iteritems():
            print k
        bt = pybacktest.Backtest(x, 'ma_cross')
        return bt

    op = pybacktest.Optimizer(strat, ohlc, processes=1)

    op.add_param('fast', 5, 20, 1)
    op.add_param('slow', 25, 50, 1)
    r = op.results()
    print r
