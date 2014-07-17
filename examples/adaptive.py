import pandas as pd
import numpy as np

def relative_strenghth(ohlc, period=2, tp=0):
    up = ohlc.C - ohlc.C.shift()
    dn = up.copy()
    up[up<0] = 0
    dn[dn>0] = 0
    dn = -dn
    return 100*pd.rolling_mean(up, period)/(pd.rolling_mean(up, period)+pd.rolling_mean(dn, period))

if __name__ == "__main__":
    RIY = ['DDD','ANF','ATVI','ADBE','AMD','A','AKAM','AA']

    rsi, ret = pd.DataFrame(), pd.DataFrame()
    for s in RIY:
        ohlc = pd.read_hdf('Data/'+s+'.h5', s)
        rsi[s] = 100 - relative_strenghth(ohlc)
        ret[s] = ohlc.C/ohlc.C.shift()-1

    wt = rsi - rsi.mean(axis=1)
    wt = wt/np.abs(wt).sum(axis=1)

    rr = (wt.shift()*ret)

    flip = 1
    for y in rr.groupby(by = lambda x: x.year):
        year = str(y[0])

        wt[year] = wt[year]*flip
        wt[year] = wt[year]/np.abs(wt[year]).sum(axis=1)

        rr[year] = wt[year].shift()*ret[year]

        flip = np.log(1+rr[year]).sum().T
        flip[flip>0]=1
        flip[flip<0]=-1
        flip.replace(np.nan, 1, inplace=True)

    r = rr.sum(axis=1)
    #eq = np.exp(np.log(1+rr).cumsum())
    #eq.plot()
    equity = np.exp(np.log(1+r).cumsum())
    equity.plot()

    long = wt[wt>=0]
    short = wt[wt<0]
    short_perf = short.shift()*ret
    long_perf = long.shift()*ret
    long_perf.count(axis=1) + short_perf.count(axis=1)

    long_wr = long_perf[long_perf>0].count(axis=1)/long_perf.count(axis=1)
    short_wr = short_perf[short_perf>0].count(axis=1)/short_perf.count(axis=1)

    equity_long = np.exp((long.shift()*ret).sum(axis=1).cumsum())
    equity_short = np.exp((short.shift()*ret).sum(axis=1).cumsum())

    daily = ret[ret>0].count(axis=1)/ret.shape[1]
    daily.plot()

    monthly = np.exp(r.groupby(lambda x : x.year*100+x.month).sum())-1
    yearly = np.exp(np.log(1+r).groupby(lambda x : x.year).sum())-1

    equity.plot(label=str(p))

    all_equity = pd.DataFrame({'Portfolio':equity, 'Long':equity_long, 'Short':equity_short})

    all_equity.plot(label='Typical Price '+str(tp))
    monthly.plot(kind='bar')
    yearly.plot(kind='bar')

