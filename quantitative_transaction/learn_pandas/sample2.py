import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from abupy import six, xrange, range, reduce, map, filter, partial, ABuMarketDrawing, ABuSymbolPd
import scipy.stats as scs


tsla_df = ABuSymbolPd.make_kl_df('usTSLA', n_folds=2)
print(tsla_df.tail())
tsla_df[['close','volume']].plot(subplots=True, style=['r','g'], grid=True)
plt.show()
print(tsla_df.info())
print(tsla_df.describe())
print(tsla_df.loc['2017-07-24':'2017-07-30','open'])
print(tsla_df.loc['2017-07-24':'2017-07-30',['open','close']])
# 项目中使用最频繁
print(tsla_df[['open','close']][0:3])




