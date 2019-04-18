from rqalpha.api import *
import string
import talib
import sys 
import os
sys.path.append("/home/wl/oneb/") 
from macd import *

def trim_order(orders):
    neworders = []
    for order in orders:
        if instruments(order).days_from_listed() > 130:
            neworders.append(order)
    return neworders


def init(context):
    context.stock = sector("Financials")
#    context.fin = all_instruments("CS")

    context.stock = trim_order(context.stock)
    print(context.stock)

    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    context.curorder = 0
    context.planorder = 0

def first_trim(context):
    context.sellout = 0
    context.planorder = 0
    curorder = context.curorder
    curslope = 0
    context.prices = {}
    context.short_avg = {}
    context.long_avg = {}
    context.volume = {}
    context.total_turnover = {}
    context.fin = context.stock

    for order in context.stock:
        context.prices[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'close')
        context.volume[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'volume')
        context.total_turnover[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'total_turnover')
        context.short_avg[order] = talib.SMA(context.prices[order], context.SHORTPERIOD)
        context.long_avg[order] = talib.SMA(context.prices[order], context.LONGPERIOD)
	
	
def before_trading(context):
    first_trim(context)
    macd_trim(context)
    
    macd_judge(context)

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
