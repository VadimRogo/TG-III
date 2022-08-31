from typing import Type
import requests
import matplotlib.pyplot as plt
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from datetime import datetime
#20.76
KEY = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
key_client = 'T4ZfheSMEw9zpet4HrDWg5NXoL7j4WrOdLl9pEObwByXYVslFK2Yman9cbAVIxwt'
secret = '7aHcuPBXfrqbIJ6AYe3ckav1Rh1G9GY59g0BBzJ6rjIZ7smvcwDi327CSdvy9IYg'
prices = []
prices12 = []
prices6 = []

client = Client(key_client, secret)
#Tiket
count = 0
Tikets = []

#Balance
MainBalanceUSDF = float(client.get_asset_balance(asset='USDT')['free'])


# RSIs 
SummOfIncomePrices = 1
SummOfLostPrices = 1
RSIs = []
RSIcounter = 0
RSIs24 = []
RSIcounters = []

#Main
MainBalancesUSD = []
priceWBuy = 0
ZeroThreePercent = 0 
Mediums = []
Counter = 0


class Indicators():
    def BuyInMin(price, prices12, prices6):
        # if price >= max(prices12):
        #     Processes.SellProcess(price, MainBalancesUSD, MainBalanceBTC)
        if price <= min(prices6):
            Type = "MinIn6"
            Processes.BuyProcess(price, PartBalance, Type)

        if price <= min(prices12):
            Type = "MinIn12"
            Processes.BuyProcess(price, PartBalance, Type)

        if price <= min(prices):
            Type = "MinInAll"
            Processes.BuyProcess(price, PartBalance, Type)

    def STOPLOSStakeprofit(price):
        #Easy mechanism name say for what is it
        for T in Tikets:
            if T['sold'] != True:
                Percent = T['price'] / 100 * 0.2
                print("Waiting price - {}".format(T['price'] + Percent))
                if T['price'] + Percent <= price:
                    Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC) 



class Processes():
    def SellAll(price):
        try:
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
                    print("Was sold {} BTC by price {}".format(quantityBTC, float(price)))
            
        except Exception as inst:
            print(inst)



    def TiketProcess(price, quantity, Type):
        #Make tiket for marks about when and how buy, need fix
        #Fix for make read that easy, tablet or something
        print('Making new Tiket')
        time = datetime.now().strftime("%H:%M:%S")
        global Tikets
        x = {
            'time' : time,
            'price' : price,
            'symbol' : 'BTCUSD',
            'quantity' : math.floor(quantity * 100000) / 100000,
            'type' : Type,
            'sold' : False
        }
        Tikets.append(x)

    def SellProcess(price, MainBalanceUSD, MainBalanceBTC):
        #Making Sell and check if system make error
        print(type(MainBalanceBTC))
        try:
            if len(Tikets) == 0:
                quantityBTC = float(MainBalanceBTC)
                order = client.create_order(
                        symbol='BTCUSDT',
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity = quantityBTC
                        )
                print("Was sold {} BTC by price {}".format(quantityBTC, float(price)))
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
                    print("Was sold {} BTC by price {}".format(quantityBTC, float(price)))
            
        except Exception as inst:
            print(inst)

    def BuyProcess(price, PartBalance, Type):
        #Making Buy and check if system give error
        global quantityBTC
        try:
            quantityBTC = math.floor(PartBalance / price * 100000) / 100000
            print('QT - ', quantityBTC, 'PartB - ', PartBalance)
            order = client.create_order(
                symbol='BTCUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantityBTC
                )
            
            Processes.TiketProcess(price, quantityBTC, Type)
            print("Was bought {} BTC by price {}".format(quantityBTC, float(price)))
        except Exception as inst:
            print("Lil error")



class MainProcesses():
    
    def CollectData(self):
        global prices6, Income, Counter, prices12, Mediums, prices, price, MainBalanceUSD, Medium, MainBalanceBTC, PartBalance
        
        #Balance
        
        MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
        MainBalanceBTC = client.get_asset_balance(asset='BTC')['free']
        MainBalancesUSD.append(MainBalanceUSD) 
        PartBalance = round(MainBalanceUSD) / 2
        if PartBalance <= 10:
            PartBalance = MainBalanceUSD 
        Income = MainBalancesUSD[0] / MainBalancesUSD[-1]
        #Data
        data = requests.get(KEY).json()
        price = round(float(data['price']), 3)
        prices.append(price)
        prices12.append(price)
        prices6.append(price)
        Medium = requests.get("https://api.binance.com/api/v3/avgPrice", params=dict(symbol="BTCUSDT")).json()
        Medium = round(float(Medium['price']), 2)
        Mediums.append(Medium)
        Percents = (prices[0] / prices[-1])


        if len(prices6) >= 6:
            prices6 = [prices6[-1]]
        if len(prices12) >= 12:
            prices = [prices12[-1]]

        #Counter
        Counter += 1
        


def MainLoop():
        #Taking data from user
        Samples = int(input('How many times check - '))
        Sec = int(input('What interval - '))
        while Samples != 0:
            Samples -= 1

            #Making Data for processes
            x = MainProcesses()
            x.CollectData()

            Indicators.BuyInMin(price, prices12, prices6)
            Indicators.STOPLOSStakeprofit(price)


            #Just for tests and trash
            print("Price - {}, Medium - {} \n".format(price, Medium))
                
            time.sleep(Sec)


MainLoop()
Processes.SellAll(price)
MainBalanceUSDE = float(client.get_asset_balance(asset='USDT')['free'])

print("Income equal {}".format(MainBalanceUSDF / MainBalanceUSDE))