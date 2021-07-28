from binance.client import Client
from binance.enums import *
import numpy as np
import config
import time

client = Client(config.API_KEY, config.API_SECRET, tld='us')
symbolTicker ='BTCUSD'
#quantity = 0.053637                  #$2177 on USD at 40400 aprox price
quantity = 0.03

btc = client.get_symbol_ticker(symbol=symbolTicker)
#print(btc)
prev_btc_price = float(btc['price'])
#print(prev_btc_price)

sellOrder = client.create_order(         #it worked
            symbol = symbolTicker,
            side = 'SELL',
            type = 'STOP_LOSS_LIMIT',
            quantity=quantity,
            price= round(prev_btc_price*0.93,2),
            stopPrice=round(prev_btc_price*0.93,2),
            timeInForce='GTC')

while 1:
    time.sleep(10)

    btc = client.get_symbol_ticker(symbol=symbolTicker)
    current_btc_price = float(btc['price'])

    print("     Prev Price = " + str(prev_btc_price))
    print("  Current Price = " + str(current_btc_price))
    print("Price different = " + str(round(current_btc_price - prev_btc_price,2)))
    print("")

    if(round(current_btc_price - prev_btc_price,2) > 20):
        print("It was fulfilled")
        print("Order cancelled")
        result = client.cancel_order(
            symbol = symbolTicker,
            orderId = sellOrder.get('orderId'))

        sellOrder = client.create_order(         #it worked
            symbol = symbolTicker,
            side = 'SELL',
            type = 'STOP_LOSS_LIMIT',
            quantity=quantity,
            price= round(current_btc_price*0.93,2),
            stopPrice=round(current_btc_price*0.93,2),
            timeInForce='GTC')
        print("New order created")
        print("")
        prev_btc_price = current_btc_price