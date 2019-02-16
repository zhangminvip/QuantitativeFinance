# coding:utf-8
import itertools
from  quantitative_transaction.test2 import *
import time
import numba as nb


def cal(keep_stock_shreshold, buy_change_shreshold):
    trade_strategy2 = TradeStrategy2()
    TradeStrategy2.set_keep_stock_threshold(keep_stock_shreshold)
    TradeStrategy2.set_buy_change_threshold(buy_change_shreshold)
    trade_loop_back = TradeLoopBack(trade_days,trade_strategy2)
    trade_loop_back.execute_trade()
    profit = 0.0 if len(trade_loop_back.profit_array) == 0 else\
        reduce(lambda a, b : a+b, trade_loop_back.profit_array)
    return profit, keep_stock_shreshold, buy_change_shreshold


keep_stock_list = list(range(2, 30, 2))
buy_change_list = [buy_change/100 for buy_change in range(-5, -16, -1)]

print('持股天数{}'.format(keep_stock_list))
print('下跌阀值{}'.format(buy_change_list))

result = []

# use numba
keep_stock_list = list(range(1, 504, 1))
# 下跌买入阀值寻找范围 -0.01 - -0.99 共99个
buy_change_list = [buy_change/100.0 for buy_change in xrange(-1, -100, -1)]

def do_single_task():
    i = 0
    start = time.clock()
    for keep_stock_shreshold, buy_change_shreshold in itertools.product(keep_stock_list, buy_change_list):
        result.append(cal(keep_stock_shreshold, buy_change_shreshold))
        i = i + 1
    end = time.clock()
    print('time: ',end - start)
    print('组合数量',i)

# do_single_task_nb = nb.jit(do_single_task)
# do_single_task()
# do_single_task_nb()  #40s





# print(sorted(result)[::-1][:10])

