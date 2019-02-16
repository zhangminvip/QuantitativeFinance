from concurrent.futures import ProcessPoolExecutor
from  quantitative_transaction.performance.use_numba import *
import time


result = []

def when_done(r):
    result.append(r.result())

start = time.clock()
with ProcessPoolExecutor() as pool:
    i= 0
    for keep_stock_threshold, buy_change_threshold in \
        itertools.product(keep_stock_list, buy_change_list):
        i = i+1
        future_result = pool.submit(cal, keep_stock_threshold,buy_change_threshold)
        future_result.add_done_callback(when_done)
    print('组合次数', i)

end = time.clock()
print('time', end-start)    # 仅需15s
print(sorted(result)[::-1][:10])
