import pdb


def gen_buy_change_list():
    buy_change_list = []
    for buy_change in range(-5, -16, -1):
        # 只针对循环执行到buy_change == -10，中断开始调试
        if buy_change == -10:
            # 打断点，通过set_trace
            # pdb.set_trace()
            pass

        buy_change = buy_change / 100
        buy_change_list.append(buy_change)
    # 故意向外抛出异常
    raise RuntimeError('debug for pdb')
    return buy_change_list

try:
    _ = gen_buy_change_list()
except Exception as e:
    # 从捕获异常的地方开始调试，经常使用的调试技巧
    # pdb.set_trace()
    pass