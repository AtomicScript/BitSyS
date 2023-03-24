from binance.client import Client
from binance.enums import *
import os
import numpy as np
import requests

MA_PERIOD_1 = 20
MA_PERIOD_2 = 90
MA_PERIOD_3 = 120

RSI_PERIOD = 14
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

API_KEY =  os.getenv('Binance_API_KEY')
API_SECRET =  os.getenv('Binance_SECRET_KEY')
client = Client(API_KEY, API_SECRET)

coin_24h_info_url = 'https://api.binance.com/api/v3/ticker/24hr'

# BTCUSDT
def get_prices(coin):
    klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, f" 51 days ago UTC")
    prices = np.array([float(kline[4]) for kline in klines])
    return prices

def get_price_change_24(coin):
    r = requests.get(coin_24h_info_url, params={'symbol':coin}) 
    info = r.json()
    price_change_percentage = float(info['priceChangePercent'])
    price_change = float(info['priceChange'])
    formated_price_change = '{:.2f}'.format(price_change)
    return f'{formated_price_change}({price_change_percentage}%)'

def get_price(coin):
    ticker = client.get_symbol_ticker(symbol=coin)
    price = float(ticker['price'])

    return price

def get_moving_average_price(coin):
    prices = get_prices(coin)
    ma_1 = np.mean(prices[-MA_PERIOD_1:])
    ma_2 = np.mean(prices[-MA_PERIOD_2:])
    ma_3 = np.mean(prices)
    return ma_1, ma_2, ma_3

def get_RSI(coin):
    prices = get_prices(coin)
    changes = np.diff(prices)
    ups = np.clip(changes, 0, np.inf)
    downs = np.clip(-changes, 0, np.inf)
    rsi = 100 - (100 / (1 + (np.mean(ups[-RSI_PERIOD:]) / np.mean(downs[-RSI_PERIOD:]))))

    if rsi > RSI_SELL_THRESHOLD:
        state = 'OverBought Potential Sell'
    elif rsi < RSI_BUY_THRESHOLD:
        state = 'OverSold Potential Buy'
    else:
        state = 'Hold'

    return rsi, state


print('Current price $' + str(get_price('BTCUSDT')) + ' Change in 24 hours ' + str(get_price_change_24('BTCUSDT')))
print(f'15D Moving average is {round(float(get_moving_average_price("BTCUSDT")[0]),2)}')
print(f'RSI : {get_RSI("BTCUSDT")[0]}, STATE : {get_RSI("BTCUSDT")[1]}')
print(f'RSI : {round(float(get_RSI("BTCUSDT")[0]))}, STATE : {get_RSI("BTCUSDT")[1]}')