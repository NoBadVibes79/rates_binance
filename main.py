import telebot
import requests
from pass_for_by import api_key, secret
from binance import Client


# Часть с ботом
bot = telebot.TeleBot('5823972005:AAHu0pyYAzrET2Ydwdv65oT_Ib4eX4nIWkg')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''👋 Привет!
💎 С помощью этого боты ты сможешь узнавать курсы USDT на бирже Binance.
💰 Так же бот автоматически считает курсы конвертации для следующих пар:
- RUB to THB
- UAH to THB
                     ''')


@bot.message_handler(commands=['get_rates'])
def send_rates(message):
    rub_usdt_rates = rub_usdt()
    uah_usdt_rates = uah_usdt()
    usdt_thb_rates = usdt_thb()
    rub_usdt_num = float(rub_usdt_rates)
    uah_usdt_num = float(uah_usdt_rates)
    usdt_thb_num = float(usdt_thb_rates)
    rub_to_thb = rub_usdt_num / usdt_thb_num
    uah_to_thb = uah_usdt_num / usdt_thb_num
    bot.send_message(message.chat.id, f"""Курс USDT на Binance:
RUB to USDT (Buy) = {rub_usdt_rates}
UAH to USDT (Buy) = {uah_usdt_rates}
USDT to THB (Sale) = {usdt_thb_rates}

Расчет по курсу:
RUB to THB = {round(rub_to_thb, 2)}
UAH to THB = {round(uah_to_thb, 2)}
                     """)


@bot.message_handler(commands=['btc'])
def send_btc(message):
    btc = float(btc_usdt())
    usdt_thb_rates = float(usdt_thb())
    btc_01 = int(btc / 10)
    bot.send_message(message.chat.id, f"""Курс BTC на Binance:
0,1 BTC = {btc_01} USDT
{btc_01} USDT = {int(btc_01 * usdt_thb_rates)} THB
                     """)


# Часть с парсером с биржи
def uah_usdt():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'fiat': 'UAH',
        'page': 1,
        'rows': 10,
        'transAmount': 5000,
        'tradeType': 'BUY',
        'asset': 'USDT',
        'countries': [],
        'proMerchantAds': False,
        'shieldMerchantAds': False,
        'publisherType': None,
        'payTypes': ['Monobank'],
    }

    response = requests.post(url=url, headers=headers, json=params).json()
    return response['data'][0]['adv']['price']


def usdt_thb():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'fiat': 'THB',
        'page': 1,
        'rows': 10,
        'transAmount': 10000,
        'tradeType': 'SELL',
        'asset': 'USDT',
        'countries': [],
        'proMerchantAds': False,
        'shieldMerchantAds': False,
        'publisherType': None,
        'payTypes': ['BANK'],
    }

    response = requests.post(url=url, headers=headers, json=params).json()
    return response['data'][0]['adv']['price']


def rub_usdt():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        "fiat": "RUB",
        "page": 1,
        "rows": 10,
        "transAmount": 20000,
        "tradeType": "BUY",
        "asset": "USDT",
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "publisherType": None,
        "payTypes": ["TinkoffNew"],
    }

    response = requests.post(url=url, headers=headers, json=params).json()
    # global rub_usdt = response['data'][0]['adv']['price']

    return response['data'][0]['adv']['price']


# Часть с запросом по Api Binance
def btc_usdt():
    client = Client(api_key, secret, {"timeout": 40})
    response = client.get_symbol_ticker(symbol="BTCUSDT")
    price = response.get('price')
    return price


if __name__ == '__main__':
    bot.polling(none_stop=True)
