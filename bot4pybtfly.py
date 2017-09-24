# -*- coding: utf-8 -*-

import pybitflyer
import json
import time

api = pybitflyer.API(api_key="your_api_key",
                     api_secret="your_secret_key")

#Optional Data 

ordside = ["BUY","SELL"]
prevorder = 0
currentorder = 0
defaultcancel = 1
maxborder = 2
minborder = -2
ordamount = 0.001

class Event(object):
    pass

class TickEvent(Event):
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask
        
    def tShow(self):
        print(self.instrument +
              ",/time :" + self.time + 
              ",/bid :" + str(self.bid) + 
              ",/ask :" + str(self.ask) + 
              ",/differ :" + str(self.ask-self.bid))

class CollEvent(Event):
    def __init__(self, evalu):
        self.type = 'Coll'
        self.evalu = evalu
        return
        
    def cShow(self):
        print("/evalu : " + str(self.evalu),"\n") 
        

def defaultSideCheck(pos, cancel, posdata):
    #///Already LONG position///
    if "BUY" in str(posdata):
        pos = 0
        cancel = 1
        return pos, cancel
    #///Already SHORT position///
    elif "SELL" in str(posdata):
        pos = 1
        cancel = 0
        return pos, cancel
    #///NOT position... [buy -> sell] order///
    else:
        pos = 0
        cancel = 1
        return pos, cancel
    
def orderClassifier(order, cancel, wl):
    if wl == True and order == 0: #WIN-Buy
        order = 0
        cancel = 1
        return order,cancel
    elif wl == True and order == 1: #WIN-Sell
        order = 1
        cancel = 0
        return order,cancel
    elif wl == False and order== 0: #LOSS-Buy
        order = 1
        cancel = 0
        return order,cancel
    elif wl == False and order == 1: #LOSS-Sell
        order = 0
        cancel = 1
        return order,cancel

def Trader():         
    
    winloss = None
    posflag = len(api.getpositions(product_code = "FX_BTC_JPY"))
    status = api.gethealth(product_code = "FX_BTC_JPY")
    getpos = api.getpositions(product_code = "FX_BTC_JPY")
    
    currentOrder, cancelOrder = defaultSideCheck(prevorder, defaultcancel, getpos)
    print(currentOrder, cancelOrder)
    while True:
        getpos = api.getpositions(product_code = "FX_BTC_JPY")
        tickData = json.dumps(api.ticker(product_code = "FX_BTC_JPY"))
        collData = json.dumps(api.getcollateral(product_code = "FX_BTC_JPY"))
        
        tdata_dict = json.loads(tickData)
        cdata_dict = json.loads(collData)
        tevent = TickEvent(tdata_dict['product_code'],
                          tdata_dict['timestamp'],
                          tdata_dict['best_bid'],
                          tdata_dict['best_ask'])
        cevent = CollEvent(cdata_dict['open_position_pnl'])
        tevent.tShow()
        cevent.cShow()
        
        if winloss is not None:
            currentOrder, cancelOrder = orderClassifier(currentOrder, cancelOrder, winloss)
            winloss = None        
        if posflag == 0 : 
            buy_btc = api.sendchildorder(product_code="FX_BTC_JPY",
                                 child_order_type="MARKET",     #LIMIT,MARKET
                                 side = ordside[currentOrder],  #[0]BUY,[1]SELL
                                 size = ordamount)
            posflag += 1    
            
        print(status,"Position :" + ordside[currentOrder])
        
        #///WIN CASE///
        if cevent.evalu >= maxborder:
            buy_btc = api.sendchildorder(product_code="FX_BTC_JPY",
                                 child_order_type="MARKET",     #LIMIT,MARKET
                                 side = ordside[cancelOrder],   #[0]BUY,[1]SELL
                                 size = ordamount)
            posflag -= 1
            winloss = True
        #///LOSS CASE///    
        elif cevent.evalu <= minborder : 
            buy_btc = api.sendchildorder(product_code="FX_BTC_JPY",
                                 child_order_type="MARKET",     #LIMIT,MARKET
                                 side = ordside[cancelOrder],   #[0]BUY,[1]SELL
                                 size = ordamount)
            posflag -= 1
            winloss = False
          
        time.sleep(1)

if __name__ == "__main__":
    Trader()