from concurrent.futures import ProcessPoolExecutor
from  quantitative_transaction.performance.test import *


result = []

def when_done(r):
    result.append(r.result())

with ProcessPoolExecutor() as pool:
    for keep_stock_threshold, buy_change_threshold in \
        itertools.product(keep_stock_list, buy_change_list):
        future_result = pool.submit(cal, keep_stock_threshold,buy_change_threshold)
        future_result.add_done_callback(when_done)

print(sorted(result)[::-1][:10])
