import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 16, 10

import pandas as pd
import math
import numpy as np

import pybacktest
import urllib2
import talib

import matplotlib.pyplot as plt

plt.figure(figsize=(18, 10))

def normalize(ohlc):
    ohlc['O'] = ohlc.O*ohlc.AC/ohlc.C
    ohlc['H'] = ohlc.H*ohlc.AC/ohlc.C
    ohlc['L'] = ohlc.L*ohlc.AC/ohlc.C
    ohlc['C'] = ohlc.AC
    return ohlc

def cci(ohlc, period = 20):
    ohlc['TP'] = (ohlc.H + ohlc.L + ohlc.C)/3
    ohlc['TPMA'] = pd.rolling_mean(ohlc.TP, period)
    mad = lambda x: np.fabs(x - x.mean()).mean()
    ohlc['MAD'] = pd.rolling_apply(ohlc.TP, period, mad)
    ohlc['CCI'] = (ohlc.TP - ohlc.TPMA)/(0.015*ohlc.MAD)
    return ohlc

def orig_eq(ohlc):
    ohlc['RET'] = np.log(ohlc.C/ohlc.C.shift())
    ohlc['CRET'] = ohlc.RET.cumsum()
    ohlc['OEQ'] = np.exp(ohlc.CRET)

def trade_cci(ohlc):
    sig = pd.Series(0, ohlc.CCI.index)
    overbought, oversold = 100, -100
    sig[ohlc.CCI>overbought] = -1
    sig[ohlc.CCI<oversold] = +1
    sig = sig.shift()
    ohlc['SIG'] = sig
    ohlc['SRET'] = ohlc.RET*sig
    return sig

def sig_to_eq(ohlc):
    #eq = np.exp(ohlc.SRET.cumsum())
    ohlc['EQ'] = np.exp(ohlc.SRET.cumsum())
    #return eq

def ticker_to_eq(ticker):
    ohlc = pybacktest.load_from_yahoo(ticker, '2008')
    normalize(ohlc)
    orig_eq(ohlc)
    cci(ohlc)
    trade_cci(ohlc)
    sig_to_eq(ohlc)
    return ohlc

# you don't need proxy part from your place
proxy = urllib2.ProxyHandler({'http': 'webproxy.wlb2.nam.nsroot.net:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
# section end
ohlc = ticker_to_eq('QQQ')

e = pd.DataFrame(ohlc.OEQ)

# AVGO does not work
NDX = ['ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','DTV','DISCA','DISH','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','GRMN','GILD','GOOGL','GOOG','HSIC','ILMN','INTC','INTU','ISRG','KLAC','GMCR','KRFT','LBTYA','LINTA','LMCA','LLTC','MAR','MAT','MXIM','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NVDA','NXPI','ORLY','PCAR','PAYX','QCOM','REGN','ROST','SNDK','SBAC','STX','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','PCLN','TSCO','TRIP','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX']

#NDX = ['ATVI', 'ADBE']

pf_eq = e.copy()
pf_eq[:] = 0
for s in NDX:
    x = ticker_to_eq(s)
    e[s] = x.EQ
    pf_eq[s] = x.SRET.fillna(value=0)

pf_eq

e.plot()
#ohlc.OEQ.plot()

e.OEQ.plot()
e['PFEQ'] = np.exp(pf_eq.cumsum()/100)
e.PFEQ.plot(secondary_y=True, style='r')
