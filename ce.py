
from rqalpha.api import *
from logbook import TimedRotatingFileHandler
from rqalpha.utils.logger import user_log as log
from rqalpha.utils.logger import user_std_handler_log_formatter, user_system_log
import string
import talib
import sys 
import os
sys.path.append("/home/wl/oneb/") 
from macd import *

user_file_handler = TimedRotatingFileHandler("/home/wl/log.txt")
user_file_handler.formatter = user_std_handler_log_formatter
log.handlers.append(user_file_handler)
user_system_log.handlers.append(user_file_handler)

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

    context.planorder = 0

def before_trading_init(context):
    context.sellout = 0 # 1 means sell out all of the stock
    context.planorder = 0
    curslope = 0
    context.prices = {}
    context.short_avg = {}
    context.long_avg = {}
    context.volume = {}
    context.total_turnover = {}
    context.fin = context.stock
    context.exe = []  #element must be a tuple of (order, "buy" or "sell", percent=0-1 )

    for order in context.stock:
        context.prices[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'close')
        context.volume[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'volume')
        context.total_turnover[order] = history_bars(order, context.LONGPERIOD+1, '1d', 'total_turnover')
        context.short_avg[order] = talib.SMA(context.prices[order], context.SHORTPERIOD)
        context.long_avg[order] = talib.SMA(context.prices[order], context.LONGPERIOD)
	
	
def before_trading(context):
    before_trading_init(context)
    macd_trim(context)
    
    macd_judge(context)

def handle_bar(context, bar_dict):
    # bar_dict[order_book_id]
    # context.portfolio 

    if context.sellout:
        for order in getcurrentorder(context):
            log.info("sellout: " + order)
            order_target_value(order, 0)
        plot("sellout", 1)
    else:
        plot("sellout", 0)

    for exe in context.exe:
        if exe[1] == 'buy':
            order = exe[0]
            shares = context.portfolio.cash / bar_dict[order].close
            log.info("cash: " + str(context.portfolio.cash) + " buy: " + order + " shares:" + str(shares))
            order_shares(order, shares)
    if context.portfolio.units == 0:
        log.info("empty")
        plot("empty", 2)
