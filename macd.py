import string
import talib

def macdslope(context, order, day):
    return context.short_avg[order][day] - context.long_avg[order][day] - (context.short_avg[order][day-1] - context.long_avg[order][day-1])
    
def macddif(context, order, day):
    return context.short_avg[order][day] - context.long_avg[order][day]

# range is [startperiod, endperiod)
# bol means bigorlittle, bol>0 means bigger, bol<0 means smaller
def macddiftrim(context, order, startperiod, endperiod, bol=1):
    old = macddif(context, order, startperiod-1)
    for i in range(startperiod, endperiod):
        new = macddif(context, order, i)
        if bol > 0 and new < old:
            return False
        elif bol < 0 and new > old:
            return False
        old = new
    return True

def macd_judge(context):
    context.sellout = 0
    context.planorder = 0
    curorder = context.curorder
    curslope = 0

    if curorder:
        curslope = macdslope(context, curorder, -1)
    for order in context.fin:
        if order == curorder:
            if macddiftrim(context, order, -2, 0, -1):
                context.sellout = 1
                print("before_trading: sellout")
        elif macddif(context, order, -1) > 0 and macddif(context, order, -2) < 0:
            slope = macdslope(context, order, -1)

            if slope > curslope and slope > 0.1:
                print("slope: " + str(slope) + " order: " + order)
                # context.sellout = 1
                context.planorder = order

def macd_trim(context):
    context.tempfin = []

    for order in context.fin:
        if macddiftrim(context, order, -2, 0):
            context.tempfin.append(order)

    context.fin = context.tempfin
    # print(len(context.fin))
