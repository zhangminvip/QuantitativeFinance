import numpy as np
import time
from abupy import six, xrange, range, reduce, map, filter, partial
import scipy.stats as scs
import matplotlib.pyplot as plt

gamblers = 100
def casino(win_rate, win_once=1, loss_once=1, commission=0.01):
    '''
    每人一万， 每人玩一百次
    :param win_rate: 输赢概率
    :param win_once:每次赢得钱数
    :param loss_once:每次输的钱数
    :param commission:手续费，默认百分之一
    :return:
    '''

    my_money = 10000
    play_cnt = 100
    commission = commission
    for _ in np.arange(0, play_cnt):
        w = np.random.binomial(1, win_rate)
        if w:
            my_money += win_once
        else:
            my_money -= loss_once

        my_money -= commission
        if my_money <= 0:
            break
    return my_money

# heaven_money = [casino(0.5, commission=0) for _ in np.arange(0,gamblers)]
# cheat_money = [casino(0.4, commission=0) for _ in np.arange(0, gamblers)]
# commission_money = [casino(0.5) for _ in np.arange(0, gamblers)]
# money = [casino(0.5,win_once=1.02,loss_once=0.98) for _ in np.arange(0, gamblers)]
money = [casino(0.45,win_once=102,loss_once=98,commission=0.01) for _ in np.arange(0, gamblers)]

# plt.hist(heaven_money)
# plt.hist(cheat_money)
# print(cheat_money)
# plt.hist(commission_money)
plt.hist(money, bins=30)
plt.show()
