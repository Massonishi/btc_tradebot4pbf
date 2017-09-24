# -*- coding: utf-8 -*-

import pybitflyer
import time

api = pybitflyer.API(api_key="your_api_key",
                     api_secret="your_secret_key")

board = api.board(product_code = "FX_BTC_JPY")     #BTC_JP / FX_BTC_JPY / ETH_BTC

minask = min([p["price"] for p in board["asks"]])
maxask = max([p["price"] for p in board["asks"]])
minbid = min([p["price"] for p in board["bids"]])
maxbid = max([p["price"] for p in board["bids"]]) 
ordSide = ["BUY","SELL"]  

print("///information///")

print("MinAsk :  {0} , MaxAsk :　{1}" .format(minask, maxask))
print("MinBid : {0} , MaxBid : {1}" .format(minbid, maxbid))

collateral = api.getcollateral()
print('''
///tradestart///
''')
buy_btc = api.sendchildorder(product_code="FX_BTC_JPY",
                             child_order_type="MARKET",     #LIMIT / MARKET
                             side = ordSide[0],                  #[0]BUY / [1]SELL
                             size = 0.001)

time.sleep(5)
print('''
///tradecomplete///
''')


                     

