import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import abupy
from abupy import six, xrange, range, reduce, map, filter, partial, ABuMarketDrawing, ABuSymbolPd, ABuIndustries, ABuScalerUtil
import scipy.stats as scs

# abupy.env.enable_example_env_ipython()

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
tsla_df = pd.read_csv('tsla_df.csv', index_col=0)
print('***')
print(tsla_df.head())
print(tsla_df.columns,'\n', tsla_df.index,tsla_df.date.dtype)


# prove that the p_change field is the result of close using the pct_change()
print(tsla_df.p_change.tail())
print(tsla_df.tail().close.pct_change())

tsla_df.p_change.hist(bins=80)
plt.show()

print('*'*50)
cats = pd.qcut(np.abs(tsla_df.p_change), 10)
print(cats)
print(cats.value_counts())


bins = [-np.inf, -7.0, -5, -3, 0, 3, 5, 7, np.inf]
cats = pd.cut(tsla_df.p_change, bins)
print(cats.value_counts())


change_ration_dummies = pd.get_dummies(cats, prefix='cr_dummies')
print(change_ration_dummies.tail())

print(cats)


# concat append merge
# tsla_df = pd.concat([tsla_df, change_ration_dummies], axis=1)
# print(tsla_df.columns)
# print(tsla_df.tail())

# print(pd.concat([tsla_df[tsla_df.p_change > 10], tsla_df[tsla_df.atr14 > 16]], axis=0))
# print(tsla_df[tsla_df.p_change > 10].append(tsla_df[tsla_df.atr14 > 16]))

# print(tsla_df.columns)

tsla_df['positive'] = np.where(tsla_df.p_change > 0, 1, 0)
print(tsla_df.head())

# building a crosstab
xt = pd.crosstab(tsla_df.date_week, tsla_df.positive)
print(xt)
xt_pct = xt.div(xt.sum(1).astype(float), axis=0)
print(xt_pct)


# crosstab histogram
xt_pct.plot(figsize=(8, 5), kind='bar', stacked=True, title='date_week -> positive', )
plt.xlabel('date_week')
plt.ylabel('positive')
plt.show()


print(tsla_df.pivot_table(['positive'], index=['date_week'], aggfunc='mean'))



print(tsla_df.groupby(['date_week','positive'])['positive'].count())

jump_threshold = tsla_df.close.median() * 0.03

print(jump_threshold)

jump_pd = pd.DataFrame()

# print(tsla_df.columns)

def judge_jump(today):
    if today.p_change > 0:
        print('p_change > 0 :',today.low- today.pre_close)
    elif today.p_change < 0:
        print('p_change < 0', today.pre_close -today.high )

    global jump_pd
    if today.p_change > 0 and (today.low - today.pre_close )> jump_threshold:
        '''符合向上跳空'''
        today['jump'] = 1
        # 向上能量=(今天最低-昨收) / 跳空阀值
        today['jump_power'] = (today.low - today.pre_close) / jump_threshold
        jump_pd = jump_pd.append(today)
    elif today.p_change < 0 and (today.pre_close - today.high) > jump_threshold:
        today['jump'] = -1
        today['jump_power'] = (today.pre_close - today.high) / jump_threshold
        jump_pd = jump_pd.append(today)

for kl_index in np.arange(0, tsla_df.shape[0]):
    today = tsla_df.ix[kl_index]
    judge_jump(today)
print(jump_pd.filter(['jump','jump_power', 'close', 'date','p_change', 'pre_close']))


r_symbol = 'usTSLA'
p_data, _ = ABuIndustries.get_industries_panel_from_target(r_symbol, show=False)
print(type(p_data))
print(p_data)

p_data_it = p_data.swapaxes('items', 'minor')
print(p_data_it)


p_data_it_close = p_data_it['close'].dropna(axis=0)
print(p_data_it_close.head())

p_data_it_close = ABuScalerUtil.scaler_std(p_data_it_close)
p_data_it_close.plot()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylabel('Price')
plt.xlabel('Time')
plt.show()









