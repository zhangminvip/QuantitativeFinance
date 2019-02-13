import six
from abc import ABCMeta, abstractmethod


class TradeStrategyBase(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def buy_strategy(self, *args, **kwargs):
        pass

    @abstractmethod
    def sell_startegy(self, *args, **kwargs):
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

    def sell_startegy(self, trade_ind, trade_day, trade_days):
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


    def _init__(self, trade_days, trade_strategy):
        self.trade_days = trade_days
        self.trade_strategy = trade_strategy
        self.profit_array = []

    def execute_trade(self):
        for ind, day in enumerate(self.trade_days):
            if self.trade_strategy.keep_stock_day > 0:
                self.profit_array.append(day.change)

            if hasattr(self.trade_strategy, 'buy_strategy'):
                self.trade_strategy.buy_strategy(ind, day, self.trade_days)

            if hasattr(self.trade_strategy, 'sell_strategy'):
                self.trade_strategy.sell_strategy(ind, day, self.trade_days)




trade_loop_back = TradeLoopBack(trade_days)