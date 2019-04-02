from rqalpha.api import *
import string
import talib

def trim_order(orders):
    neworders = []
    for order in orders:
        if instruments(order).days_from_listed() > 130:
            neworders.append(order)
    return neworders


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = "000001.XSHE"
    context.fin = sector("Financials")
#    context.fin = all_instruments("CS")

    print(context.fin)
    context.fin = trim_order(context.fin)
    print(context.fin)

    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    context.curorder = 0
    context.maxorder = 0

def before_trading(context):
    context.sellout = 0
    context.maxorder = 0
    curorder = context.curorder
    curslope = 0
    prices = {}
    short_avg = {}
    long_avg = {}
    for order in context.fin:
        prices[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'close')
        short_avg[order] = talib.SMA(prices[order], context.SHORTPERIOD)
        long_avg[order] = talib.SMA(prices[order], context.LONGPERIOD)
    if curorder:
        curslope = short_avg[curorder][-1] - long_avg[curorder][-1] - (short_avg[curorder][-2] - long_avg[curorder][-2])
    for order in context.fin:
        if order == curorder:
            if short_avg[order][-1] - long_avg[order][-1] < 0 and short_avg[order][-2] - long_avg[order][-2] > 0:
                context.sellout = 1
                print("before_trading: sellout")
        elif short_avg[order][-1] - long_avg[order][-1] > 0 and short_avg[order][-2] - long_avg[order][-2] < 0:
            slope = short_avg[order][-1] - long_avg[order][-1] - (short_avg[order][-2] - long_avg[order][-2])
            if slope > curslope and slope > 0.1:
                print("slope: " + str(slope) + " order: " + order)
                context.maxorder = order
                context.sellout = 1


def handle_bar(context, bar_dict):
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    if context.sellout and context.curorder != 0:
        print("sellout: " + str(context.curorder))
        order_target_value(context.curorder, 0)
        context.curorder = 0
        plot("sellout", 1)
    if context.maxorder:
        shares = context.portfolio.cash / bar_dict[context.maxorder].close
        print("cash: " + str(context.portfolio.cash) + " buy: " + context.maxorder + " shares:" + str(shares))
        order_shares(context.maxorder, shares)
        context.curorder = context.maxorder
    if context.portfolio.units == 0:
        print("empty")
        plot("empty", 2)
