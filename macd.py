import string
import talib

def macdslope(short_avg, long_avg, order):
    return short_avg[order][-1] - long_avg[order][-1] - (short_avg[order][-2] - long_avg[order][-2])

def macd_judge(context):
    context.sellout = 0
    context.planorder = 0
    curorder = context.curorder
    curslope = 0

    if curorder:
        curslope = macdslope(context.short_avg, context.long_avg, curorder)
    for order in context.fin:
        if order == curorder:
            if context.short_avg[order][-1] - context.long_avg[order][-1] < 0 and context.short_avg[order][-2] - context.long_avg[order][-2] > 0:
                context.sellout = 1
                print("before_trading: sellout")
        elif context.short_avg[order][-1] - context.long_avg[order][-1] > 0 and context.short_avg[order][-2] - context.long_avg[order][-2] < 0:
            slope = macdslope(context.short_avg, context.long_avg, order)

            if slope > curslope and slope > 0.1:
                print("slope: " + str(slope) + " order: " + order)
                context.sellout = 1
                context.planorder = order

def macd_trim(context):
    context.newfin = []

    for order in context.fin:
        if context.short_avg[order][-1] - context.long_avg[order][-1] > 0 and context.short_avg[order][-2] - context.long_avg[order][-2] < 0:
            slope = macdslope(context.short_avg, context.long_avg, order)
            if slope > 0:
                context.newfin.append(order)

    #context.fin = context.newfin
