import requests
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from datetime import datetime

KEY = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
key = 'T4ZfheSMEw9zpet4HrDWg5NXoL7j4WrOdLl9pEObwByXYVslFK2Yman9cbAVIxwt'
secret = '7aHcuPBXfrqbIJ6AYe3ckav1Rh1G9GY59g0BBzJ6rjIZ7smvcwDi327CSdvy9IYg'
prices = []

client = Client(key, secret)
#Tiket
count = 0
Tikets = []
# RSIs 
SummOfIncomePrices = 1
SummOfLostPrices = 1
RSIs = []


class Indicators():
    def RSI(price, prices, balance):
        global SummOfIncomePrices
        global SummOfLostPrices
        global RSIs
        
        if price > prices[len(prices) - 2]:
            SummOfIncomePrices += price
        elif price < prices[len(prices) - 2]:
            SummOfLostPrices += price
        RS = SummOfIncomePrices / SummOfLostPrices
        
        RSI = 100 - 100 / (1 + RS)
        print("RSI - {}".format(RSI))
        RSIs.append(RSI)
        if RSI <= 80 and RSI >= 70:
            Processes.SellProcess(price)
        if balance > 0:
            if RSI <= 35 and RSI >= 25:
                Processes.BuyProcess(price)

class Processes():
 
    def TiketProcess(price):
        count += 1
        time = datetime.now().strftime("%H:%M:%S")
        global Tikets
        x = {
            'time' : time,
            'price' : price,
            'symbol' : 'ETHUSDT',
            'sold' : False
        }
        Tikets.append(x)




    def SellProcess(price):
        try:
            global Tikets
            quantityETH = 0.007
            order = client.create_order(
                symbol='ETHUSDT',
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity = quantityETH
                )
            print("Was sold 0.007 ETH by price {price}")
            for Tik in Tikets:
                if Tik['sold'] == False:
                    Tik['sold'] = True
        except Exception as inst:
            print(inst)

    def BuyProcess(price):
        try:
            buy_quantity = 0.007 
            order = client.create_order(
                symbol='ETHUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=buy_quantity
                )
            print("Was bought 0.007 ETH by price {price}")
            Processes.TiketProcess(price)
        except Exception as inst:
            print(inst)


    def CheckPriceProcess(price):
        try:
            for Tik in Tikets:
                if Tik['sold'] == 'False':
                    print('Waiting for {}'.format(price + price / 100 * 0.3))
                    if Tik['price'] >= price + price / 100 * 0.3:
                        Processes.SellProcess(price)   
        except Exception as inst:
            print(inst)
counter = 0

def MainLoop():
    
    while True:
        global counter
        MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
        data = requests.get(KEY).json()
        price = round(float(data['price']), 3)
        prices.append(price)
            
        if counter > 0:
            Indicators.RSI(price, prices, MainBalanceUSD)
        Processes.CheckPriceProcess(price)

        print(Tikets)
        counter += 1
        print(price)
        time.sleep(5)




        
MainLoop()