from rqalpha.api import *
import string
import talib

def trim_order(orders):
    neworders = []
    for order in orders:
        if instruments(order).days_from_listed() > 130:
            neworders.append(order)
    return neworders


def init(context):
    context.fin = sector("Financials")
#    context.fin = all_instruments("CS")

    context.fin = trim_order(context.fin)
    print(context.fin)

    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    context.curorder = 0
    context.planorder = 0
def macdslope(short_avg, long_avg, order):
    return short_avg[order][-1] - long_avg[order][-1] - (short_avg[order][-2] - long_avg[order][-2])


def macd_trim(context):
    context.sellout = 0
    context.planorder = 0
    curorder = context.curorder
    curslope = 0
    prices = {}
    short_avg = {}
    long_avg = {}
    volume = {}
    total_turnover = {}
    for order in context.fin:
        prices[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'close')
        volume[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'volume')
        total_turnover[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'total_turnover')
        short_avg[order] = talib.SMA(prices[order], context.SHORTPERIOD)
        long_avg[order] = talib.SMA(prices[order], context.LONGPERIOD)
    if curorder:
        curslope = macdslope(short_avg, long_avg, curorder)
    for order in context.fin:
        if order == curorder:
            if short_avg[order][-1] - long_avg[order][-1] < 0 and short_avg[order][-2] - long_avg[order][-2] > 0:
                context.sellout = 1
                print("before_trading: sellout")
        elif short_avg[order][-1] - long_avg[order][-1] > 0 and short_avg[order][-2] - long_avg[order][-2] < 0:
            slope = macdslope(short_avg, long_avg, order)
            if slope > curslope and slope > 0.1:
                print("slope: " + str(slope) + " order: " + order)
                context.planorder = order
                context.sellout = 1
        
def before_trading(context):
    macd_trim(context)

def handle_bar(context, bar_dict):
    # bar_dict[order_book_id]
    # context.portfolio 

    if context.sellout and context.curorder != 0:
        print("sellout: " + str(context.curorder))
        order_target_value(context.curorder, 0)
        context.curorder = 0
        plot("sellout", 1)
    if context.planorder:
        shares = context.portfolio.cash / bar_dict[context.planorder].close
        print("cash: " + str(context.portfolio.cash) + " buy: " + context.planorder + " shares:" + str(shares))
        order_shares(context.planorder, shares)
        context.curorder = context.planorder
    if context.portfolio.units == 0:
        print("empty")
        plot("empty", 2)
