from concurrent.futures import process
from multiprocessing.dummy import Process
from statistics import median
from urllib import request
import requests
import matplotlib.pyplot as plt
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
RSIs24 = []


#Main

priceWBuy = 0
ZeroThreePercent = 0 
Mediums = []
Counter = 0

class Indicators():
    def CheckMinMax(price):
        #Easy process
        if price == min(prices):
            Processes.BuyProcess(price, PartBalance)
        if price == max(prices):
            Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)

    def STOPLOSStakeprofit(price):
        #Easy mechanism name say for what is it
        for T in Tikets:
            ZeroThreePercent = T['price'] / 100 * 0.3
            ThreePercent = T['price'] / 100 * 0.3
            if T['price'] + ZeroThreePercent < price:
                Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC) 
            elif price  > T['price'] + ThreePercent:
                Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)
    def CheckRandom(price):
        #Just for fun
        rand = random.randint(0, 100)
        if rand < 10:
            Processes.SellProcess(price, MainBalanceBTC, MainBalanceBTC)
        if rand > 90:
            Processes.BuyProcess(price, PartBalance)

    def Fibonachi(maxprice, minprice, price):
        #Fibo need to think about that so situative Process
        diff = maxprice - minprice
        precent = diff / 100


        Firstlevel = maxprice - 23.6 * precent
        Secondlevel = maxprice - 38.2 * precent
        Thirdlevel = maxprice - 50 * precent
        Fourlevel = maxprice - 61.8 * precent
        Final = maxprice
        if MainBalanceUSD >= 10:
            if price > Firstlevel - 5 and price < Firstlevel + 5:
                Processes.BuyProcess(price, PartBalance)
                print("FIBONACHI - ", price)

            if price > Secondlevel - 5 and price < Secondlevel + 5:
                Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)
                print("FIBONACHI - ", price)


            if price > Thirdlevel - 5 and price < Thirdlevel + 5:
                Processes.BuyProcess(price, PartBalance)
                print("FIBONACHI - ", price)

            if price > Fourlevel - 5 and price < Thirdlevel + 5:
                Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)
                print("FIBONACHI - ", price)

    def RSI(price, prices, MainBalanceUSD, MainBalanceBTC, PartBalance):
        #RSI Process need check errors because 50 can't be so often how it now
        global RSIs24, SummOfIncomePrices, RSIcounter, RSIs, SummOfLostPrices

        RSIcounter += 1
        if price > prices[len(prices) - 2]:
            SummOfIncomePrices += price
        elif price < prices[len(prices) - 2]:
            SummOfLostPrices += price
        RS = SummOfIncomePrices / SummOfLostPrices
        
        RSI = 100 - 100 / (1 + RS)
        print("RSI - {}".format(RSI))
        RSIs24.append(RSI)
        RSIs.append(RSI)
        if len(RSIs) == 24:
            SummOfIncomePrices = 1
            SummOfLostPrices = 1
            RSIs24 = [50]
            
        if RSI <= 80 and RSI >= 70 and Counter >= 15:
            Processes.SellProcess(price, MainBalanceUSD, MainBalanceBTC)
        if MainBalanceUSD >= 10 and Counter >= 15:
            if RSI <= 35 and RSI >= 25:
                Processes.BuyProcess(price, PartBalance)

    def CheckMedium(Medium, price, PartBalance):
        #Need more work for and check information about EMA and MA
        if Medium > price - 3 and Medium < price + 5:
            Processes.BuyProcess(price, PartBalance)


    

class Processes():

    def MakingPlot():
        #Making Graph need fix, for make read graph easy
        Times = range(0, Counter)
        
        plt.subplot(1, 2, 1)
        plt.plot(Times, prices)
        plt.plot(Times, Mediums)
        plt.subplot(1, 2, 2)
        plt.plot(Times, RSIs)
        plt.show()


    def TiketProcess(price, quantity):
        #Make tiket for marks about when and how buy, need fix
        #Fix for make read that easy, tablet or something
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
        #Making Sell and check if system make error
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
        #Making Buy and check if system give error
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
        global Counter, Mediums, prices, price, MainBalanceUSD, Medium, MainBalanceBTC, PartBalance
        
        #Balance
        MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
        MainBalanceBTC = client.get_asset_balance(asset='BTC')['free']
        PartBalance = round(MainBalanceUSD) / 2
        if PartBalance <= 10:
            PartBalance = MainBalanceUSD 
        
        #Data
        data = requests.get(KEY).json()
        price = round(float(data['price']), 3)
        prices.append(price)
        Medium = requests.get("https://api.binance.com/api/v3/avgPrice", params=dict(symbol="BTCUSDT")).json()
        Medium = round(float(Medium['price']), 2)
        Mediums.append(Medium)

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


            #Working Indicators
            Indicators.RSI(price, prices, MainBalanceUSD, MainBalanceBTC, PartBalance)
            Indicators.Fibonachi(max(prices), min(prices), price)
            Indicators.CheckMedium(Medium, price, PartBalance)
            Indicators.STOPLOSStakeprofit(price, Tikets, MainBalanceUSD, MainBalanceBTC)
            Indicators.CheckMinMax(price)
            Indicators.CheckRandom(price)

            #Just for tests and trash
            print(price)    
            print(Medium)
            time.sleep(Sec)
            
        

MainLoop()
print('Done')
Processes.MakingPlot()

