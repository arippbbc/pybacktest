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
    #trade_cci(ohlc)
    #sig_to_eq(ohlc)
    return ohlc
# you don't need proxy part from your place
proxy = urllib2.ProxyHandler({'http': 'webproxy.wlb2.nam.nsroot.net:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
# section end
ohlc = ticker_to_eq('IWB')
e = pd.DataFrame(ohlc.OEQ)
r = pd.DataFrame(ohlc.OEQ)

# AVGO does not work
RIY = ['DDD','MMM','AAN','ABT','ABBV','ANF','ACN','ACE','ACT','ATVI','ADBE','ADT','AAP','AMD','ACM','AES','AET','AMG','AFL','AGCO','A','GAS','AL','APD','ARG','AKAM','ALK','ALB','AA','ALR','ARE','ALXN','ALKS','Y','ATI','ALLE','AGN','ADS','LNT','ATK','AWH','ALSN','MDRX','ALL','ALTR','MO','AMZN','AMCX','DOX','UHAL','AEE','AAL','ACC','AGNC','ACAS','AEO','AEP','AXP','AFG','AMH','AIG','ANAT','AMT','AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','NLY','ANSS','AR','AOS','AOL','AON','APA','AIV','APOL','AAPL','AMAT','ATR','WTR','ACGL','ADM','ARCC','ARIA','AWI','ARW','AJG','APAM','ASNA','ASH','AHL','ASBC','AIZ','AGO','T','ATML','ATO','ATW','ADSK','ADP','AN','AZO','AVGO','AVB','AVY','CAR','AVT','AVP','AVX','AXS','BEAV','BWC','BHI','BLL','BYI','BAC','BOH','BK','BKU','BAX','BBT','BEAM','BDX','BBBY','BMS','BRK/B','BBY','BIG','BIO','BIIB','BMRN','BMR','BLK','BA','BOKF','BAH','BWA','BXP','BSX','BDN','BRE','EAT','BMY','BRX','BRCM','BR','BRCD','BKD','BRO','BF/B','BRKR','BG','BKW','CA','CAB','CVC','CBT','COG','CDNS','CPN','CPT','CAM','CPB','COF','CSE','CAH','CFN','CSL','KMX','CCL','CRS','CRI','CTRX','CAT','CBL','CBOE','CBG','CBS','CDW','CE','CELG','CNP','CTL','CERN','CF','CHRW','CRL','SCHW','CHTR','LNG','CHK','CVX','CBI','CHS','CIM','CMG','CHH','CB','CHD','CI','XEC','CINF','CNK','CTAS','CSCO','CIT','C','CTXS','CYN','CLH','CCO','CLF','CLX','CME','CMS','CNA','COH','CIE','KO','CCE','CTSH','CFX','CL','CMCSA','CMA','CBSH','CWH','COMM','CYH','CMP','CSC','CPWR','CNW','CAG','CXO','CNQR','COP','CNX','ED','STZ','CLR','COO','CPA','CPRT','CLGX','GLW','OFC','CXW','COST','COTY','CVD','CVA','COV','BCR','CR','CREE','CCI','CCK','CST','CSX','CBST','CFR','CMI','CVI','CVS','CYT','DHR','DRI','DVA','DDR','DF','DECK','DE','DLPH','DAL','DNR','XRAY','DVN','DV','DO','DKS','DBD','DLR','DDS','DTV','DFS','DISCA','DISH','DLB','DG','DLTR','D','DPZ','UFS','DCI','DEI','DOV','DOW','DHI','DPS','DWA','DRC','DRQ','DST','DSW','DTE','DUK','DRE','DNB','DNKN','ETFC','EXP','EWBC','EMN','ETN','EV','EBAY','SATS','ECL','EIX','EW','DD','EA','LLY','EMC','EMR','ENDP','ENH','EGN','ENR','ETR','EVHC','EOG','EQT','EFX','EQIX','ELS','EQR','ERIE','ESS','EL','RE','XLS','EXC','EXPE','EXPD','ESRX','EXR','XOM','FFIV','FB','FDS','FCS','FDO','FAST','FRT','FII','FDX','FNF','FIS','FITB','FEYE','FCNCA','FHN','FNFG','FRC','FSLR','FE','FISV','FLT','FLIR','FLO','FLS','FLR','FMC','FTI','FL','F','FCE/A','FRX','FTNT','FBHS','FOSL','FI','BEN','FCX','FSL','TFM','FTR','FULT','GME','GLPI','GCI','GPS','GRMN','IT','GMT','GD','GE','GGP','GIS','GM','GWR','G','GNTX','GPC','GNW','GILD','GPN','GNC','GLNG','GS','GT','GOOG','GGG','GHC','GXP','GEF','GRPN','GES','GPOR','HRB','HAL','HBI','THG','HOG','HAR','HRS','HSC','HIG','HAS','HTS','HE','HCA','HCC','HCP','HDS','HCN','HNT','HTA','HP','HSIC','HLF','HSY','HTZ','HES','HPQ','HXL','HRC','HSH','HFC','HOLX','HD','HME','AWAY','HON','HRL','HSP','HPT','HST','HHC','HUB/B','HCBK','HUM','HBAN','HII','HUN','H','IACI','IEX','IDXX','IHS','ITW','ILMN','INCY','INFA','VOYA','IR','IM','INGR','TEG','INTC','I','IBKR','ICE','IBM','IFF','IGT','IP','IPG','INTU','ISRG','IVZ','IPGP','IRM','ITC','ITT','JBL','JKHY','JEC','JAH','JAZZ','JBHT','JCP','JDSU','SJM','JW/A','JNJ','JCI','JLL','JOY','JPM','JNPR','KSU','KAR','KBR','K','KMPR','KMT','GMCR','KEY','KRC','KMB','KIM','KMI','KEX','KLAC','KN','KSS','KOS','KRFT','KR','KRO','LB','LLL','LH','LRCX','LAMR','LSTR','LPI','LVS','LAZ','LEA','LM','LEG','LDOS','LEN','LII','LUK','LVLT','LXK','LBTYK','LBTYA','LINTA','LMCA','LPT','LVNTA','LPNT','LECO','LNC','LLTC','LNKD','LGF','LKQ','LMT','L','LO','LOW','LPLA','LSI','LYB','MTB','MAC','CLI','M','MSG','MNK','MTW','MAN','MRO','MPC','MKL','MAR','MMC','MLM','MRVL','MAS','MA','MAT','MXIM','MBI','MKC','MDR','MCD','MHFI','MCK','MDU','MJN','MWV','MDVN','MD','MDT','MRK','MCY','MET','MTD','MFA','MGM','KORS','MCHP','MU','MCRS','MSFT','MAA','MHK','TAP','MDLZ','MON','MNST','MCO','MS','MORN','MOS','MSI','MRC','MSM','MSCI','MUR','MUSA','MYL','MYGN','NBR','NDAQ','NFG','NATI','NOV','NNN','NSM','NAV','NCR','NTAP','NFLX','N','NSR','NYCB','NWL','NFX','NEU','NEM','NWSA','NEE','NLSN','NKE','NI','NBL','NDSN','JWN','NSC','NU','NTRS','NOC','NCLH','NRG','NUS','NUAN','NUE','NVDA','NVR','ORLY','OAS','OXY','OII','OCN','OGE','OIS','ODFL','ORI','OHI','OCR','OMC','ONNN','OGS','OKE','ORCL','OSK','OC','OI','PCAR','PKG','PLL','PANW','P','PNRA','PH','PRE','PDCO','PTEN','PAYX','PBF','BTU','PENN','PNR','PBCT','POM','PEP','PKI','PRGO','PETM','PFE','PCG','PCYC','PM','PSX','PDM','PF','PNW','PXD','PBI','PCL','PNC','PII','PLCM','BPOP','PPS','PPG','PPL','PX','PCP','PINC','PCLN','PFG','PRA','PG','PGR','PLD','PL','PRU','PEG','PSA','PHM','PVH','QEP','QGEN','QCOM','PWR','DGX','STR','Q','RAX','RL','RRC','RJF','RYN','RTN','RLGY','O','RHT','RGC','RBC','REG','REGN','RF','RGA','RS','RNR','RSG','RMD','RPAI','RAI','RVBD','RHI','RKT','ROK','COL','ROC','ROL','ROP','ROST','ROVI','RDC','RCL','RGLD','RES','RPM','RRD','R','SWY','CRM','SLXP','SBH','SNDK','SD','SBAC','SCG','SLB','SAIC','SMG','SNI','SDRL','SEE','SHLD','SGEN','SEAS','SEIC','SRE','SNH','SCI','NOW','SHW','SIAL','SBNY','SIG','SLGN','SLAB','SPG','SIRI','SIRO','SIX','SWKS','SLG','SLM','SM','SNA','SCTY','SWI','SLH','SON','SO','SCCO','LUV','SWN','SE','SPR','SRC','SPLK','S','SFM','SPW','JOE','STJ','SFG','SWK','SPLS','SBUX','HOT','STWD','SWAY','STRZA','STT','STLD','SRCL','SSYS','SYK','STI','SPN','SIVB','SYMC','SNPS','SNV','SYY','TROW','TMUS','DATA','TAHO','SKT','TGT','TCO','TMHC','TCB','AMTD','TECD','TECH','TE','TK','TFX','TDS','TPX','THC','TDC','TER','TEX','TSLA','TSO','TXN','TXT','TFSL','THRX','TMO','TRI','THO','TIBX','TDW','TIF','TWC','TWX','TKR','TJX','TOL','TMK','TTC','TSS','TW','TSCO','TDG','TRV','TRMB','TRN','TRIP','TGI','TRW','TUP','TWTC','FOXA','TWTR','TWO','TSN','UDR','UGI','ULTA','UPL','UA','UNP','UNT','UAL','UPS','URI','USM','X','UTX','UTHR','UNH','UHS','UNM','URBN','URS','USB','VLO','VR','VLY','VMI','VAL','VNTV','VAR','WOOF','VVC','VEEV','VTR','PAY','VRSN','VRSK','VZ','VRTX','VFC','VIAB','V','VSH','VC','VMW','VNO','VMC','WBC','WAB','WDR','WMT','WAG','DIS','WAFD','WCN','WM','WAT','WTW','WRI','WLP','WFC','WEN','WCC','WR','WDC','WU','WLK','WY','WHR','WTM','WWAV','WLL','WFM','WMB','WSM','WIN','WEC','WDAY','INT','WPC','WPX','WRB','GRA','GWW','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YHOO','YUM','ZBRA','ZMH','ZION','ZTS','ZU','ZNGA']

pf_eq = e.copy()
pf_eq[:] = 0
for s in RIY:
    # these three symbol could not be found by free server
    if s not in ['BEAM', 'BRE', 'LSI']:
        x = ticker_to_eq(s)
        #x.fillna(0, inplace=True)
        e[s] = x.CCI
        r[s] = x.RET
        #pf_eq[s] = x.SRET.fillna(value=0)

# e contains cci of all symbols, i didn't name it cci cause I want it to be generic, drop unnecessary column
e = e.drop('OEQ', 1)
# r is the log return of all symbols, drop unnecessary column
r = r.drop('OEQ', 1)

# m is the cci mean of all symbols, row by row, or day by day
m = e.mean(axis = 1)

# adjust cci to be cci minus mean of all cci day by day
e = e-m

# f is taking absolute value of adjusted cci
f = np.abs(e)

# x is the sum of absolute adjusted cci
x = f.sum(axis = 1)

# weighted by sum(absolute adjusted cci)
e = e/x

# return for each symbol is log return*weight, then sum by each row to get portfolio return for that day
# shift signal by one day back
p = (e.shift()*r).sum(axis = 1)

# equity curve is exp of cumulative log return
eq = np.exp(p.cumsum())

eq.plot()
ohlc.OEQ.plot()

