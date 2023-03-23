from binance.client import Client
from binance.enums import *
import os
import numpy as np
import requests


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

while True:
    print('Current price $' + str(get_price('BTCUSDT')) + ' Change in 24 hours ' + str(get_price_change_24('BTCUSDT')))