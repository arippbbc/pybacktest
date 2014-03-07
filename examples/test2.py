import pybacktest
     ...: import numpy as np
     ...: import pandas as pd
     ...: import datetime as dt
     ...: e = pd.read_csv("data/ecb/eur.csv", dtype={'Time':object})
     ...: e.Time = pd.to_datetime(e.Time, format='%Y-%m-%d %H:%M:%S:%f')
     ...: e.plot()
     ...: 
     ...: f = e.copy()
     ...: f.index = f.Time
     ...: x = [str(s)[:-7] for s in f.index]
     ...: ff = f.set_index(pd.Series(x))
     ...: ff.index.name = 'Time'
     ...: ff.plot()
