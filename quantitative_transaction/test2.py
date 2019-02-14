#coding:utf-8
import sys
from collections import namedtuple
from collections import OrderedDict
sys.path.append('..')
import abupy
from abupy import six, xrange, range, reduce, map, filter, partial
# abupy.env.enable_example_env_ipython()


class StockTradeDays(object):
    def __init__(self, price_array, start_date, date_array=None):
        self._price_array = price_array
        self._date_array = self._init_days(start_date, date_array)
        self._change_array = self.__init_change()
        self.stock_dict = self._init_stock_dict()


    def __init_change(self):
        price_float_array = [float(price_str) for price_str in self._price_array]
        pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
        change_array = list(map(lambda pp:reduce(lambda a, b:round((b-a)/a,3),pp), pp_array))
        change_array.insert(0,0)
        return change_array


    def _init_days(self, start_date, date_array):
        if date_array is None:
            date_array = [str(start_date + ind) for ind, _ in enumerate(self._price_array)]
        else:
            date_array = [str(date) for date in date_array ]
        return date_array

    def _init_stock_dict(self):
        stock_namedtuple = namedtuple('stock',('date', 'price','change'))
        stock_dict = OrderedDict(
            (date, stock_namedtuple(date,price, change))
                                 for date, price, change in zip(self._date_array, self._price_array, self._change_array))
        return stock_dict

    def filter_stock(self, want_up=True, want_calc_sum=False):
        """
        筛选结果子集
        :param want_up: 是否筛选上涨
        :param want_calc_sum: 是否计算涨跌和
        :return:
        """
        # Python中的三目表达式的写法
        filter_func = (lambda p_day: p_day.change > 0) if want_up else (
            lambda p_day: p_day.change < 0)
        # 使用filter_func做筛选函数
        want_days = list(filter(filter_func, self.stock_dict.values()))

        if not want_calc_sum:
            return want_days

        # 需要计算涨跌幅和
        change_sum = 0.0
        for day in want_days:
            change_sum += day.change
        return change_sum


    def __str__(self):
        return str(self.stock_dict)

    __repr__ = __str__

    def __iter__(self):
        for key in self.stock_dict:
            yield self.stock_dict[key]

    def __getitem__(self, ind):
        date_key = self._date_array[ind]
        return self.stock_dict[date_key]

    def __len__(self):
        return len(self.stock_dict)

price_array = '30.14,29.58,26.36,32.56,32.82'.split(',')
date_base = 20170118
trade_days = StockTradeDays(price_array, date_base)
print(trade_days)

from collections import  Iterable
if isinstance(trade_days, Iterable):
    for day in trade_days:
        print(day)

print(trade_days.filter_stock())

from abupy import ABuSymbolPd
# 两年的TSLA收盘数据 to list
price_array = ABuSymbolPd.make_kl_df('WB', n_folds=2).close.tolist()
# 两年的TSLA收盘日期 to list，这里的写法不考虑效率，只做演示使用
date_array = ABuSymbolPd.make_kl_df('WB', n_folds=2).date.tolist()
print(price_array[:5], date_array[:5])
trade_days = StockTradeDays(price_array, date_base, date_array)
print('trade_days对象长度为: {}'.format(len(trade_days)))
print('最后一天交易数据为：{}'.format(trade_days[-1]))



import six
from abc import ABCMeta, abstractmethod


class TradeStrategyBase(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def buy_strategy(self, *args, **kwargs):
        pass

    @abstractmethod
    def sell_strategy(self, *args, **kwargs):
        pass

class TradeStrategy1(TradeStrategyBase):

    s_keep_stock__threshold = 20

    def __init__(self):
        self.keep_stock_threshold = 0
        self.__buy_change_threshold = 0.07

    def buy_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_threshold == 0 and \
            trade_day.change > self.__buy_change_threshold:
            self.keep_stock_threshold += 1
        elif self.keep_stock_threshold > 0:
            self.keep_stock_threshold += 1

    def sell_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_threshold >= \
            TradeStrategy1.s_keep_stock__threshold:
            self.keep_stock_threshold = 0


    @property
    def buy_change_threshold(self):
        return self.__buy_change_threshold

    @buy_change_threshold.setter
    def buy_change_threshold(self, buy_change_threshold):
        if not isinstance(buy_change_threshold, float):
            raise TypeError('buy_change_threshold must be float')
        self.__buy_change_threshold = round(buy_change_threshold, 2)



class TradeLoopBack(object):


    def __init__(self, trade_days, trade_strategy):
        self.trade_days = trade_days
        self.trade_strategy = trade_strategy
        self.profit_array = []

    def execute_trade(self):
        for ind, day in enumerate(self.trade_days):
            if self.trade_strategy.keep_stock_threshold > 0:
                self.profit_array.append(day.change)

            if hasattr(self.trade_strategy, 'buy_strategy'):
                self.trade_strategy.buy_strategy(ind, day, self.trade_days)

            if hasattr(self.trade_strategy, 'sell_strategy'):
                self.trade_strategy.sell_strategy(ind, day, self.trade_days)



# TradeStrategy1()
trade_loop_back = TradeLoopBack(trade_days,TradeStrategy1())
trade_loop_back.execute_trade()
print('回测策略1，总盈亏为：{}%'.format(reduce(lambda a,b: a + b , trade_loop_back.profit_array)* 100))
# print(trade_loop_back.profit_array)
# print(trade_days.filter_stock())
print(1)
print(len(trade_days))
print(len(trade_loop_back.profit_array))

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

sns.set_context(rc={'figure.figsize': (14, 7)} )
plt.plot(np.array(trade_loop_back.profit_array).cumsum())
plt.show()


trade_strategy1 = TradeStrategy1()

trade_strategy1.buy_change_threshold = 0.1
trade_loop_back = TradeLoopBack(trade_days, trade_strategy1)
trade_loop_back.execute_trade()
print('修改change阀值后')
print(len(trade_days))
print(len(trade_loop_back.profit_array))
print('回测策略1,总盈亏为：{}%'.format(reduce(lambda a, b : a+b, trade_loop_back.profit_array)*100))

plt.plot(np.array(trade_loop_back.profit_array).cumsum())
plt.show()


class TradeStrategy2(TradeStrategyBase):
    '''
    交易策略2, 均值回复策略
    '''
    #买入后持有天数
    s_keep_stock_threshold = 10

    # 下跌买入阀值
    s_buy_change_threshold = -0.1

    def __init__(self):
        self.keep_stock_threshold = 0

    def buy_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_threshold == 0 and trade_ind >=1:
            today_down = trade_day.change < 0
            yesterday_down = trade_days[trade_ind - 1].change < 0
            down_rate = trade_day.change + \
                trade_days[trade_ind - 1].change
            if today_down and yesterday_down and down_rate < TradeStrategy2.s_buy_change_threshold:
                self.keep_stock_threshold += 1
        elif self.keep_stock_threshold > 0:
            self.keep_stock_threshold += 1


    def sell_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_threshold >=\
            TradeStrategy2.s_keep_stock_threshold:
            self.keep_stock_threshold = 0


    @classmethod
    def set_keep_stock_threshold(cls, keep_stock_threshold):
        cls.s_keep_stock_threshold = keep_stock_threshold

    @staticmethod
    def set_buy_change_threshold(buy_change_threshold):
        TradeStrategy2.s_buy_change_threshold = buy_change_threshold


trade_strategy2 = TradeStrategy2()
trade_loop_back = TradeLoopBack(trade_days, trade_strategy2)
trade_loop_back.execute_trade()
print('回测策略2 总盈亏为：{}%'.format(reduce(lambda a, b: a + b, trade_loop_back.profit_array) * 100))
plt.plot(np.array(trade_loop_back.profit_array).cumsum());
plt.show()



# 实例化一个新的TradeStrategy2类对象
trade_strategy2 = TradeStrategy2()
# 修改为买入后持有股票20天，默认为10天
TradeStrategy2.set_keep_stock_threshold(20)
# 修改股价下跌买入阀值为-0.08（下跌8%），默认为-0.10（下跌10%）
TradeStrategy2.set_buy_change_threshold(-0.08)
# 实例化新的回测对象trade_loop_back
trade_loop_back = TradeLoopBack(trade_days, trade_strategy2)
# 执行回测
trade_loop_back.execute_trade()
print('回测策略2 总盈亏为：{}%'.format(reduce(lambda a, b: a + b, trade_loop_back.profit_array) * 100))
# 可视化回测结果
plt.plot(np.array(trade_loop_back.profit_array).cumsum())
plt.show()



