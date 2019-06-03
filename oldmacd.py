import string
import talib
from rqalpha.utils.logger import user_log as log

# return a list []
def getcurrentorder(context):
    a = context.portfolio.stock_account.positions
    return a
    
def macdslope(context, order, day):
    return context.short_avg[order][day] - context.long_avg[order][day] - (context.short_avg[order][day-1] - context.long_avg[order][day-1])
   
# get macd dif value
def macddif(context, order, day):
    return context.short_avg[order][day] - context.long_avg[order][day]

# get macd dea value

# range is [startperiod, endperiod)
# bol means bigorlittle, bol>0 means bigger, bol<0 means smaller
def macddiftrim(context, order, startperiod, endperiod, bol=1):
    old = macddif(context, order, startperiod-1)
    for i in range(startperiod, endperiod):
        new = macddif(context, order, i)
        if bol > 0 and new <= old:
            return False
        elif bol < 0 and new >= old:
            return False
        old = new
    return True

def macd_judge(context):
    for order in getcurrentorder(context):
        if macddiftrim(context, order, -2, 0, -1):
            context.exe.append([order, "sell", 1])
            log.info("before_trading: sell " + order)

    for order in context.stocks:
        if macddif(context, order, -1) > 0 and macddif(context, order, -2) < 0:
            slope = macdslope(context, order, -1)

            if slope > 0.1:
                log.info("slope: " + str(slope) + " order: " + order)
                context.sellout = 1
                context.exe.append([order, "buy", 1])

def macd_trim(context):
    tempstock = []

    for order in context.stocks:
        if macddiftrim(context, order, -2, 0):
            tempstock.append(order)

    context.stocks = tempstock
    # print(len(context.fin))
