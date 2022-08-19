import requests
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException


key = 'T4ZfheSMEw9zpet4HrDWg5NXoL7j4WrOdLl9pEObwByXYVslFK2Yman9cbAVIxwt'
secret = '7aHcuPBXfrqbIJ6AYe3ckav1Rh1G9GY59g0BBzJ6rjIZ7smvcwDi327CSdvy9IYg'
symbols = ["BTC","LTC","ETH","NEO","BNB","QTUM","EOS","SNT","BNT","GAS","BCC","USDT","HSR","OAX","DNT","MCO","ICN","ZRX","OMG","WTC","YOYO","LRC","TRX","SNGLS","STRAT","BQX","FUN","KNC","CDT","XVG","IOTA","SNM","LINK","CVC","TNT","REP","MDA","MTL","SALT","NULS","SUB","STX","MTH","ADX","ETC","ENG","ZEC","AST","GNT","DGD","BAT","DASH","POWR","BTG","REQ","XMR","EVX","VIB","ENJ","VEN","ARK","XRP","MOD","STORJ","KMD","RCN","EDO","DATA","DLT","MANA","PPT","RDN","GXS","AMB","ARN","BCPT","CND","GVT","POE","BTS","FUEL","XZC","QSP","LSK","BCD","TNB","ADA","LEND","XLM","CMT","WAVES","WABI","GTO","ICX","OST","ELF","AION","WINGS","BRD","NEBL","NAV","VIBE","LUN","TRIG","APPC","CHAT","RLC","INS","PIVX","IOST","STEEM","NANO","AE","VIA","BLZ","SYS","RPX","NCASH","POA","ONT","ZIL","STORM","XEM","WAN","WPR","QLC","GRS","CLOAK","LOOM","BCN","TUSD","ZEN","SKY","THETA","IOTX","QKC","AGI","NXS","SC","NPXS","KEY","NAS","MFT","DENT","IQ","ARDR","HOT","VET","DOCK","POLY","VTHO","ONG","PHX","HC","GO","PAX","RVN","DCR","USDC","MITH","BCHABC","BCHSV","REN","BTT","USDS","FET","TFUEL","CELR","MATIC","ATOM","PHB","ONE","FTM","BTCB","USDSB","CHZ","COS","ALGO","ERD","DOGE","BGBP","DUSK","ANKR","WIN","TUSDB","COCOS","PERL","TOMO","BUSD","BAND","BEAM","HBAR","XTZ","NGN","DGB","NKN","GBP","EUR","KAVA","RUB","UAH","ARPA","TRY","CTXC","AERGO","BCH","TROY","BRL","VITE","FTT","AUD","OGN","DREP","BULL","BEAR","ETHBULL","ETHBEAR","XRPBULL","XRPBEAR","EOSBULL","EOSBEAR","TCT","WRX","LTO","ZAR","MBL","COTI","BKRW","BNBBULL","BNBBEAR","HIVE","STPT","SOL","IDRT","CTSI","CHR","BTCUP","BTCDOWN","HNT","JST","FIO","BIDR","STMX","MDT","PNT","COMP","IRIS","MKR","SXP","SNX","DAI","ETHUP","ETHDOWN","ADAUP","ADADOWN","LINKUP","LINKDOWN","DOT","RUNE","BNBUP","BNBDOWN","XTZUP","XTZDOWN","AVA","BAL","YFI","SRM","ANT","CRV","SAND","OCEAN","NMR","LUNA","IDEX","RSR","PAXG","WNXM","TRB","EGLD","BZRX","WBTC","KSM","SUSHI","YFII","DIA","BEL","UMA","EOSUP","TRXUP","EOSDOWN","TRXDOWN","XRPUP","XRPDOWN","DOTUP","DOTDOWN","NBS","WING","SWRV","LTCUP","LTCDOWN","CREAM","UNI","OXT","SUN","AVAX","BURGER","BAKE","FLM","SCRT","XVS","CAKE","SPARTA","UNIUP","UNIDOWN","ALPHA","ORN","UTK","NEAR","VIDT","AAVE","FIL","SXPUP","SXPDOWN","INJ","FILDOWN","FILUP","YFIUP","YFIDOWN","CTK","EASY","AUDIO","BCHUP","BCHDOWN","BOT","AXS","AKRO","HARD","KP3R","RENBTC","SLP","STRAX","UNFI","CVP","BCHA","FOR","FRONT","ROSE","HEGIC","AAVEUP","AAVEDOWN","PROM","BETH","SKL","GLM","SUSD","COVER","GHST","SUSHIUP","SUSHIDOWN","XLMUP","XLMDOWN","DF","JUV","PSG","BVND","GRT","CELO","TWT","REEF","OG","ATM","ASR","1INCH","RIF","BTCST","TRU","DEXE","CKB","FIRO","LIT","PROS","VAI","SFP","FXS","DODO","AUCTION","UFT","ACM","PHA","TVK","BADGER","FIS","OM","POND","ALICE","DEGO","BIFI","LINA"]


client = Client(key, secret)

info = client.get_account()
status = client.get_account_status()

# print(type(info))

orders = client.get_all_orders(symbol='BTCUSDT', limit=10)
MainBalanceUSD = client.get_asset_balance(asset='USDT')
# balanceBTC = client.get_asset_balance(asset='BTC')
# balanceLINKUP = client.get_asset_balance(asset = 'LINKUP')

exchange_info = client.get_exchange_info()

# for i in symbols:
#     balance = client.get_asset_balance(asset=i)
#     print(balance)
#     time.sleep(3)

#First get ETH price
eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
tikets = []

buy_quantity = float(MainBalanceUSD['free']) / float(eth_price['price'])
buy_quantity = round(buy_quantity/2, 3)
print(buy_quantity)


# Create test order
class Tik:
    def __init__(self, num, symbol, quantity, price, sell):
        self.num = num
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.sell = sell

    def MakingTiket(num, symbol, quantity, price, sell):
        x = {
            'num' : num,
            'symbol' : symbol,
            'quantity' : quantity,
            'price' : price,
            'sell' : sell
        }
        tikets.append(x)
        
def BuyOrder():
    try:
        global tikets
        eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
        if float(MainBalanceUSD['free']) > 10:
            buy_quantity = round(float(MainBalanceUSD['free']) / float(eth_price['price'])/2, 3)
            
            tiket = Tik.MakingTiket(random.randint(100, 1000), 'ETHUSDT', buy_quantity, eth_price, False) 
            order = client.create_order(
                symbol='ETHUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=buy_quantity
                )
    except Exception as inst:
        print(inst)


def SellOrder(tikets):
    
    for i in tikets:
        print(i['quantity'])
        # if i['sell'] == False:
        #     order = client.create_test_order(
        #     symbol='ETHUSDT',
        #     side=Client.SIDE_SELL,
        #     type=Client.ORDER_TYPE_MARKET,
        #     quantity=i['quantity']
        #     )


while True:
    BuyOrder()
    SellOrder(tikets)
    time.sleep(6)
 # T


# for s in exchange_info['symbols']:
#     print(s['symbol'])
#     balance = client.get_asset_balance(asset=s['symbol'])
#     print(balance)
#     # print(s['symbol'])
