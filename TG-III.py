from concurrent.futures import process
from multiprocessing.dummy import Process
import requests
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from datetime import datetime

KEY = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
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
RSIcounter = 0


#Main
counter = 0
priceWBuy = 0
ZeroThreePercent = 0 


class Indicators():
    

    def RSI(price, prices, MainBalanceUSD, MainBalanceBTC, PartBalance):
        global SummOfIncomePrices, RSIcounter, RSIs, SummOfLostPrices

        RSIcounter += 1
        if price > prices[len(prices) - 2]:
            SummOfIncomePrices += price
        elif price < prices[len(prices) - 2]:
            SummOfLostPrices += price
        RS = SummOfIncomePrices / SummOfLostPrices
        
        RSI = 100 - 100 / (1 + RS)
        print("RSI - {}".format(RSI))
        RSIs.append(RSI)

        if RSI <= 80 and RSI >= 70 and counter >= 15:
            Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)
        if MainBalanceUSD >= 10 and counter >= 15:
            if RSI <= 35 and RSI >= 25:
                Processes.BuyProcess(price, PartBalance)

    def Madium(prices):
        Medium = sum(prices) / len(prices)
        return Medium

class Processes():

    def TiketProcess(price, quantity):
        print('Making new Tiket')
        time = datetime.now().strftime("%H:%M:%S")
        global Tikets
        x = {
            'time' : time,
            'price' : price,
            'symbol' : 'BTCUSD',
            'quantity' : math.floor(quantity * 10000) / 10000,
            'sold' : False
        }
        Tikets.append(x)

    def SellProcess(price, MainBalanceUSD, MainBalanceBTC):
        try:
            if len(Tikets) == 0:
                quantityBTC = MainBalanceBTC
                order = client.create_order(
                        symbol='BTCUSDT',
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity = quantityBTC
                        )


            for T in Tikets:
                if T['sold'] == False:
                    T['sold'] = True
                    quantityBTC = T['quantity']        
                    order = client.create_order(
                        symbol='BTCUSDT',
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity = quantityBTC
                        )
                    print("Was sold 0.00054 BTC by price {}".format(float(price)))
            
        except Exception as inst:
            print(inst)
            print(MainBalanceUSD)

    def BuyProcess(price, PartBalance):
        try:
            quantityBTC = math.floor(PartBalance / price * 100000) / 100000
            print('QT - ', quantityBTC, 'PartB - ', PartBalance)
            order = client.create_order(
                symbol='BTCUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantityBTC
                )
            
            Processes.TiketProcess(price, quantityBTC)
            print("Was bought {} BTC by price {}".format(quantityBTC, float(price)))
        except Exception as inst:
            print(inst)
            print(MainBalanceUSD)
            print(quantityBTC * price)
        

class MainProcesses():
    def CollectData(self):
        global prices, price, MainBalanceUSD, MainBalanceBTC, PartBalance
        MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
        MainBalanceBTC = client.get_asset_balance(asset='BTC')['free']
        PartBalance = round(MainBalanceUSD) / 2
        if PartBalance <= 10:
            PartBalance = MainBalanceUSD 
        data = requests.get(KEY).json()
        price = round(float(data['price']), 3)
        prices.append(price)
        


def MainLoop():
    c = 0
    while True:
        c += 1
        x = MainProcesses()
        x.CollectData()
        Indicators.RSI(price, prices, MainBalanceUSD, MainBalanceBTC, PartBalance)

        time.sleep(900)
        

MainLoop()
print(Tikets)
