from rqalpha.api import *
import string
import talib


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = "000001.XSHE"
    context.fin = sector("Financials")
    print(context.fin)
#    context.fin = all_instruments("CS")
    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    context.maxslope = 0
    context.curorder = 0
    context.maxorder = 0

def before_trading(context):
    context.sellout = 0
    prices = {}
    short_avg = {}
    long_avg = {}
    for order in context.fin:
      if instruments(order).days_from_listed() > 130:
        prices[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'close')
        short_avg[order] = talib.SMA(prices[order], context.SHORTPERIOD)
        long_avg[order] = talib.SMA(prices[order], context.LONGPERIOD)
    for order in context.fin:
      if instruments(order).days_from_listed() > 130:
        if short_avg[order][-1] - long_avg[order][-1] > 0 and short_avg[order][-2] - long_avg[order][-2] < 0:
            slope = short_avg[order][-1] - long_avg[order][-1] - (short_avg[order][-2] - long_avg[order][-2])
            print("slope: ")
            print(slope)
            if order == context.curorder:
                context.sellout = 0
                return
            if slope > context.maxslope and slope > 0.1:
                context.maxslope = slope
                context.maxorder = order
                print("order: " + order)
                context.sellout = 1


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！


    if context.sellout and context.curorder != 0:
        print("sellout: " + str(context.curorder))
        order_target_value(context.curorder, 0)
    # 计算现在portfolio中的现金可以购买多少股票
    if context.maxorder and context.sellout == 1:
        shares = context.portfolio.cash / bar_dict[context.maxorder].close

        print("cash: " + str(context.portfolio.cash) + " buy: " + context.maxorder)
        print(shares)
        order_shares(context.maxorder, shares)
        context.curorder = context.maxorder
#    if context.maxorder:
#        plot("avg", short_avg[context.maxorder] - long_avg[context.maxorder])
