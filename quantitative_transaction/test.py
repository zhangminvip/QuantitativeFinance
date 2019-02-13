#coding:utf-8
from __future__ import print_function
import sys
sys.path.append('..')
import abupy
from collections import OrderedDict
from collections import namedtuple


from abupy import six, xrange, range, reduce, map, filter, partial
# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()


print(sys.version)
# stock_name = ['a','us']
# stock_price = [1,2]
# z = zip(stock_name, stock_price)
# for name, price in z:
#     print(name, price)


price_str = '30.14, 29.58, 26.36, 32.56, 32.82'
if not isinstance(price_str, str):
    # not代表逻辑‘非’， 如果不是字符串，转换为字符串
    price_str = str(price_str)
if isinstance(price_str, int) and price_str > 0:
    # and 代表逻辑‘与’，如果是int类型且是正数
    price_str += 1
elif isinstance(price_str, float) or float(price_str[:4]) < 0:
    # or 代表逻辑‘或’，如果是float或者小于0
    price_str += 1.0
else:
    try:
        raise TypeError('price_str is str type!')
    except TypeError:
        print('raise, try except')


print('旧的price_str id= {}'.format(id(price_str)))
price_str = price_str.replace(' ', '')
print('新的price_str id= {}'.format(id(price_str)))
price_str

# split以逗号分割字符串，返回数组price_array
price_array = price_str.split(',')
print(price_array)
# price_array尾部append一个重复的32.82
price_array.append('32.82')
print(price_array)

set(price_array)
price_array.remove('32.82')


date_array = []
date_base = 20170118
# 这里用for只是为了计数，无用的变量python建议使用'_'声明
for _ in xrange(0, len(price_array)):
    # 本节只是简单示例，不考虑日期的进位
    date_array.append(str(date_base))
    date_base += 1
print(date_array)

stock_dict = {date:price for date, price in zip(date_array, price_array)}
stock_dict = OrderedDict((date, price) for date, price in zip(date_array, price_array))
print(stock_dict['20170119'])
print(stock_dict.keys())
print(stock_dict.values())



print(min(zip(stock_dict.values(), stock_dict.keys())))
# print(min())

find_second_max_lambd = lambda dict_array:sorted(zip(dict_array.values(), dict_array.keys()))[-2]
print(find_second_max_lambd(stock_dict))
print(stock_dict)

price_float_array = [float(price_str) for price_str in stock_dict.values()]
print(price_float_array)
print(price_float_array[:-1])
print(price_float_array[1:])
pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
print(pp_array)

change_array = list(map(lambda pp:reduce(lambda a, b :round((b-a)/a, 3),pp),pp_array))
change_array.insert(0,0)
print(change_array)

stock_namedtuple = namedtuple('stock',('date', 'price','change'))
stock_dict = OrderedDict((date, stock_namedtuple(date, price, change)) for date, price, change in zip(date_array, price_array, change_array))
# print(stock_dict.values())
print('*'*10)
# print(stock_dict)
for key in stock_dict:
    print(key)
up_days = list(filter(lambda day: day.change > 0, stock_dict.values()))
print(up_days)

def filter_stock(stock_array_dict, want_up=True, want_calc_sum=False):
    if not isinstance(stock_array_dict, OrderedDict):
        raise TypeError('stock_array_dict is not OrderdDict')
    filter_func = (lambda day: day.change > 0) if want_up else (lambda day: day.change < 0)
    want_days = list(filter(filter_func, stock_array_dict.values()))

    if not want_calc_sum:
        return want_days

    change_sum = 0.0
    for day in want_days:
        change_sum += day.change
    return change_sum

print('all up days :{}'.format(filter_stock(stock_dict)))
print('all down days:{}'.format(filter_stock(stock_dict, want_up=False)))
print('the sum of all up days:{}'.format(filter_stock(stock_dict, want_calc_sum=True )))
print('the sum of all down days:{}'.format(filter_stock(stock_dict, want_calc_sum=True, want_up=False)))
