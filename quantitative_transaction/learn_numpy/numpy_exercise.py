import numpy as np
import time
from abupy import six, xrange, range, reduce, map, filter, partial
import scipy.stats as scs
import matplotlib.pyplot as plt

# start_normal = time.clock()
# normal_list = range(1000)
# [i ** 2 for i in normal_list]
# end_normal = time.clock()
# print(end_normal - start_normal)
#
# start_normal = time.clock()
# np_list = np.array(1000)
# np_list ** 2
# end_normal = time.clock()
# print(end_normal - start_normal)
#
# # 注意 * 3的操作被运行在每一个元素上
# np_list = np.ones(5) * 3
# print(np_list)
# # 普通的列表把*3操作认为是整体性操作
# normal_list = [1, 1, 1, 1, 1] * 3
# print(normal_list)
#
# print(np.zeros(100))
#
# print(np.zeros((3, 2)))
#
# print(np.empty((2, 3, 3)))
# print(np.zeros_like(np_list))
# print(np.ones_like(np_list))
# print(np.eye(4))
#
# data = [[1, 2, 3, 4], [5, 6, 7, 8]]
# arr_np = np.array(data)
# print(arr_np)
# print(np.linspace(0, 1, 10))
#
# stock_cnt = 200
# view_days = 504
# stock_day_change = np.random.standard_normal((stock_cnt, view_days))
# print(stock_day_change.shape)
#
# # price_float_array = [100, 120, 130, 90,80,100]
# # pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
# # print(pp_array)
# # change_array = list(map(lambda pp:reduce(lambda a, b:round((b-a)/a,3),pp), pp_array))
# # print(change_array)
# # print(sum(change_array))
#
#
# print(stock_day_change[:1, :5])
# print('倒数', stock_day_change[-2:, -5:])
# print('保留两位小数', np.around(stock_day_change[-2:, -5:], 2))
#
# print('转换成int', stock_day_change[-2:, -5:].astype(int))
#
# tmp_test = stock_day_change[-2:, -5:].copy()
# tmp_test[0][0] = np.nan
# print('stock_day_change', stock_day_change[-2:, -5:])
# print('tmp_test', tmp_test)
#
# print('原始数据', stock_day_change[0:2, 0:5])
# mask = stock_day_change[0:2, 0:5] > 0.5
# print('涨幅大于0.5', mask)
# tmp_test = stock_day_change[0:2, 0:5]
# print('选择后', tmp_test[mask])
#
# print('一行写完', tmp_test[tmp_test > 0.5])
#
# print('多重筛选条件', tmp_test[(tmp_test > 1) | (tmp_test < -1)])
#
# print('前', stock_day_change[:2, :5])
# print('后', stock_day_change[-2:, -5:])
# print(np.maximum(stock_day_change[:2, :5], stock_day_change[-2:, -5:]))
#
# print('唯一', np.unique(stock_day_change[-2:, -5:].astype(int)))
#
# print('diff', np.diff(stock_day_change[:2, :5], axis=0))
# print('where', np.where(stock_day_change[:2, :5] > 0.5))
# print('where', np.where(stock_day_change[:2, :5] > 0.5, 1, stock_day_change[:2, :5]))
#
# print('where 多重条件', np.where(np.logical_or(tmp_test > 0.5, tmp_test < -0.5), 1, tmp_test))
# print('where 多重条件 ', np.where(np.logical_and(tmp_test > 0.5, tmp_test < 1), 1, tmp_test))
#
# np.save('stock_day_change', stock_day_change)
# stock_day_change = np.load('stock_day_change.npy')
# print(stock_day_change.shape)
#
# stock_day_change_four = stock_day_change[:4, :4]
# print(stock_day_change_four)
#
# print('最大涨幅{}'.format(np.max(stock_day_change_four[:2, :], axis=1)))
# print('最大跌幅{}'.format(np.min(stock_day_change_four, axis=1)))
# print('振幅幅度{}'.format(np.std(stock_day_change_four, axis=1)))
# print('平均涨跌{}'.format(np.mean(stock_day_change_four, axis=1)))
#
# print('最大涨幅{}'.format(np.max(stock_day_change_four, axis=0)))
# print('最大涨幅{}'.format(np.argmax(stock_day_change_four, axis=0)))
#
# a_investor = np.random.normal(loc=100, scale=50, size=(100, 1))
# b_investor = np.random.normal(loc=100, scale=50, size=(100, 1))
#
# print('a交易者期望{0:.2f},标准差{1:.2f},方差{2:0.2f}'.format(a_investor.mean(), a_investor.std(), a_investor.var()))
# print('b交易者期望{0:.2f},标准差{1:.2f},方差{2:0.2f}'.format(b_investor.mean(), b_investor.std(), b_investor.var()))
#
# a_mean = a_investor.mean()
# a_std = a_investor.std()
#
# plt.plot(a_investor)
# plt.axhline(a_mean + a_std, color='r')
# plt.axhline(a_mean - a_std, color='y')
# plt.show()
# # print(a_investor)
#
# print(np.linspace(1, 20))
#
# import scipy.stats as scs
#
# stock_mean = stock_day_change[0].mean()
# stock_std = stock_day_change[0].std()
#
# print('股票0 mean 均值期望{:.3f}'.format(stock_mean))
# print('股票0 stdf 标准差{:.3f}'.format(stock_std))
#
# print(stock_day_change[0])
# plt.hist(stock_day_change[0], bins=50, normed=True)
#
# fit_linspace = np.linspace(stock_day_change[0].min(), stock_day_change[0].max())
# # print(fit_linspace.shape)
# pdf = scs.norm(stock_mean, stock_std).pdf(fit_linspace)
# plt.plot(fit_linspace, pdf, lw=2, c='r')
# plt.show()


stock_cnt = 200
view_days = 504
stock_day_change = np.random.standard_normal((stock_cnt, view_days))
print(stock_day_change)

keep_day = 50
stock_day_change_test = stock_day_change[:stock_cnt, 0:view_days-keep_day]

print('前测试天数盈亏总和:',np.sort(np.sum(stock_day_change_test, axis=1))[:3])

stock_lower_array = np.argsort(np.sum(stock_day_change_test, axis=1))[:3]
print('最小的三个序号',stock_lower_array)


def show_buy_lower(stock_ind):
    '''

    :param stock_ind: 股票序号
    :return:
    '''
    # 设置一个一行两列的可视化图表
    _, axs = plt.subplots(nrows=1, ncols=2, figsize= (16, 5))
    axs[0].plot(np.arange(0, view_days - keep_day), stock_day_change_test[stock_ind].cumsum())
    cs_buy = stock_day_change[stock_ind][view_days - keep_day : view_days].cumsum()
    axs[1].plot(np.arange(view_days-keep_day, view_days), cs_buy)
    plt.show()
    print('stock_ind:{}, mean{:.2f},后{}天总和{:.2f}'.format(stock_ind, stock_day_change[stock_ind].mean(), keep_day, cs_buy[-1]))
    return cs_buy[-1]

# 最后输出的盈亏比例
profit = 0

# 遍历跌幅最大的三只股票序号序列
for stock_ind in stock_lower_array:
    profit += show_buy_lower(stock_ind)
print(profit)


# print(np.array([1,2,3]).cumsum())

# print(np.sum(np.array([1,2,3])))
# print(np.array([1,2,3]).mean())
