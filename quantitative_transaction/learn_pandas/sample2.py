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

print(tsla_df.columns)


# get abs, multiple logic
print(tsla_df[(np.abs(tsla_df.p_change )>8) & (tsla_df.volume > 2.5 * tsla_df.volume.mean())])


# sort_index loc
print(tsla_df.sort_index(by='p_change', ascending=False).loc['2017-03-3':'2017-03-22',['open','close']])

# iloc
print(tsla_df.sort_index(by='p_change', ascending=False).iloc[1:2,2:3])

# series slice
print(tsla_df.open.pct_change()[:3])



# series pct_change function
print('*'*20)
change_ratio = tsla_df.close.pct_change()
print(type(change_ratio))
print(change_ratio.tail())


# np round function
print(np.round(change_ratio[-5:], 2))

# series map function
format = lambda x: '%.2f' % x
print(change_ratio.map(format).tail())
print(tsla_df.close.map(format).tail())




# save as csv, save index and columns by default.
# tsla_df.to_csv('tsla_df.csv', columns=tsla_df.columns, index=True)
tsla_df.to_csv('tsla_df.csv')

# specify column 0 to be the index, convert the object to datetime
tsla_df = pd.read_csv('tsla_df.csv', index_col=0, parse_dates=True)
print('***')
print(tsla_df.head())
print(tsla_df.columns,'\n', tsla_df.index,tsla_df.date.dtype)







