# oneb
I want to earn my first one b...

rqalpha update-bundle
rqalpha run -d ./rqalpha/bundle/ -s 2016-06-01 -e 2019-03-24 --account stock 100000 --benchmark 000300.XSHG --plot -f oneb/ce.py


先调用getstock把想要限定的股票池放到一个文件中，stocks.txt
rqalpha run -d ./rqalpha/bundle/ -s 2016-06-01 -e 2019-03-24 --account stock 100000 --benchmark 000300.XSHG --plot -f oneb/get_stocks.py

回测类型，ce_type.txt
选择回测类型，写入ce_type.txt


然后再执行，对特定股票池回测
rqalpha run -d ./rqalpha/bundle/ -s 2016-06-01 -e 2019-03-24 --account stock 100000 --benchmark 000300.XSHG --plot -f oneb/ce_stocks.py


context
	
##############################################
	get_stocks.py
	macd_stocks.py
先使用rqalpha选股，而不是作回测
选股方法：
1、选定周线图已经作大回调，并且企稳的迹象
	周线图（或者三日均线）上5日线稳定，macd企稳，

选股应该使用windows上的软件选择，而不是自己写软件



