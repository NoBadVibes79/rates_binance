import telebot
import requests
from binance import Client
import json

api_key = 'YOU_BINANCE_API_KEY'
secret = 'YOU_BINANCE_SECRET_KEY'
TOKEN = 'YOU_TELEGRAM_TOKEN'

# Часть с ботом
bot = telebot.TeleBot(f'{TOKEN}')


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


# Парсинг с Bybit
def rub_usdt():
    cookies = {
        '_abck': 'A4359B24B37FD14FE81B1A80C9CF9984~-1~YAAQj2pkXzrVWEmKAQAAN3v4TwoYSh3bbXxJ+kJICdb7hAwOU0C11p+MleR+Cw3Br16PHL33e2WhNO7cLJqhnyHbWqTnQWLxI0Zf1G886kticErqDgTV//G/0Hmnf6I4LW/iWBYYob0tsY7EKkqDixdyS90J3BAWHPxpzhyvAoJEdxmQwTulVr8SPHJDBWN6jYssooRyZLQdz66kZpyf93FlijUn8wsNMCZx6KQ/Swc1GHwQRDEfo5F9F+KhnQnv95KEGeMDzOCMG9COZrEw5YUiSUjvk9TW64TnG2c5za4c5yMl5EA8YBdYOLrvkiQYKz9tP4X/IpcLN0ROLN9ucgH0ML1uIiLY4KPT6BAzaW+mLNUcuEFWY3de7g==~-1~-1~-1',
        'bm_sz': '55C4954475B0323A89D0ED770D2B5724~YAAQj2pkXz3VWEmKAQAAN3v4TxT8+94DNyhCk/D1rXEGgCsncrUkqsD64Xh9XDb6tohOAnX2QSp3uAUuddco6Y7m9ZdugckMhQ6KxUjtqhD+C+zxOvTCZG4Xwd1jvY9fZyqbDJD4NuUqjl211nSh8Qu6wkty4XVTaJctvEcd5gl7K3nkFWRwgKZ7BK/nPfztxzjG5DxLjECyz5hYcAVR7ZHVmtCP4tpTvWlIPlZvuff9VR7UuhiXlVAZ6iKMs9T9qnVwQrpT31xhkBo6ar+zz1gaPz2Y0ohUZYOETtIu3OoE5Q==~3555637~3748404',
        '_gcl_au': '1.1.560795829.1693558800',
        'deviceId': '623f8bee-ebf1-c86c-65dc-aa056a3cee71',
        '_ga': 'GA1.1.636144554.1693558800',
        '_ga_SPS4ND2MGC': 'GS1.1.1693558800.1.0.1693558800.0.0.0',
        '_ym_uid': '1693558800995501144',
        '_ym_d': '1693558800',
        '_ym_isad': '1',
        '_by_l_g_d': '584de78c-b7c7-d2c0-6f3a-e7cbbe143525',
        'BYBIT_REG_REF_prod': '{"lang":"ru-RU","g":"584de78c-b7c7-d2c0-6f3a-e7cbbe143525","medium":"direct","url":"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=64"}',
        'sajssdk_2015_cross_new_user': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218a4ff880d4fd8-05bfbc937d5dc3-26031f51-2073600-18a4ff880d5899%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_a_u_v%22%3A%220.0.5%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThhNGZmODgwZDRmZDgtMDViZmJjOTM3ZDVkYzMtMjYwMzFmNTEtMjA3MzYwMC0xOGE0ZmY4ODBkNTg5OSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218a4ff880d4fd8-05bfbc937d5dc3-26031f51-2073600-18a4ff880d5899%22%7D',
        'ak_bmsc': '70FC0A382730428AD9B09487F5384F62~000000000000000000000000000000~YAAQj2pkX/nVWEmKAQAAd4j4TxQpdUWOWVJiYvQNgnFQSKekvWIr+DnPz6scmBbXJzAL90Sztl+VLbbQU34BDmDPAlFjs34ZI3KRTBD/eCdfByUV9Vxzxf0bxGhgVo8dgh+BKbD9/cH3WJQ7Bq3mjFR5d0ZhryGH6BSTucdbitwRwf4FytS0RkCUE4/tplBZTePU6c9cvGOA0mpuCNizTIy5EctI1GTaQmQBKJ+2KNXgKoSeISIEIIsfgxZChE9QU4pRK79eIWpgVgvraUjdPn3V1KilwRs9bGWrGNP4lDcdTLOyTdeVMCDTFLVOj+JDAP4zDMoMNw/pok2D9pbPGliTw16H3DA1kMTYfJ60f51SrcOCQdc83VuNvtR0iDer+gS4vp9NDD96eu5P0FsbhiI49Ahc4EkZVs7jbmuemDu2RYQPphHQTL8fD5kOS+ruNuTDE8h+eYITahbthwIBOn8Z7uoKJJMxSV+m8nJJfEMHKRRTJgkhNz6PRQ53W8o=',
        'b_t_c_k': '',
        'bm_sv': '2D19E595422E9C69D08683472613026F~YAAQj2pkX33eWEmKAQAAcmP5TxRw65uU6WvIXTdhwGvkuYvSg2cOTi6npjFa/Z+yn48h80J5ijV6iy4FqFJbfFGG2oSn+/acYc3I6RGdVJdGy40uoV+KI23bsuYBV4wOL88STthvzr+xr/lual5FfgdgUDevmk6hL+yZ95xqWjPMJzujxZQPIUwuoZDkQ276tmRTjpMqPUnM7M1olJqIp/ab9UM6KZBRQDDgBPp70/cy1BX2MHGA4IVxBM5sdfXq~1',
    }

    headers = {
        'authority': 'api2.bybit.com',
        'accept': 'application/json',
        'accept-language': 'ru-RU',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': '_abck=A4359B24B37FD14FE81B1A80C9CF9984~-1~YAAQj2pkXzrVWEmKAQAAN3v4TwoYSh3bbXxJ+kJICdb7hAwOU0C11p+MleR+Cw3Br16PHL33e2WhNO7cLJqhnyHbWqTnQWLxI0Zf1G886kticErqDgTV//G/0Hmnf6I4LW/iWBYYob0tsY7EKkqDixdyS90J3BAWHPxpzhyvAoJEdxmQwTulVr8SPHJDBWN6jYssooRyZLQdz66kZpyf93FlijUn8wsNMCZx6KQ/Swc1GHwQRDEfo5F9F+KhnQnv95KEGeMDzOCMG9COZrEw5YUiSUjvk9TW64TnG2c5za4c5yMl5EA8YBdYOLrvkiQYKz9tP4X/IpcLN0ROLN9ucgH0ML1uIiLY4KPT6BAzaW+mLNUcuEFWY3de7g==~-1~-1~-1; bm_sz=55C4954475B0323A89D0ED770D2B5724~YAAQj2pkXz3VWEmKAQAAN3v4TxT8+94DNyhCk/D1rXEGgCsncrUkqsD64Xh9XDb6tohOAnX2QSp3uAUuddco6Y7m9ZdugckMhQ6KxUjtqhD+C+zxOvTCZG4Xwd1jvY9fZyqbDJD4NuUqjl211nSh8Qu6wkty4XVTaJctvEcd5gl7K3nkFWRwgKZ7BK/nPfztxzjG5DxLjECyz5hYcAVR7ZHVmtCP4tpTvWlIPlZvuff9VR7UuhiXlVAZ6iKMs9T9qnVwQrpT31xhkBo6ar+zz1gaPz2Y0ohUZYOETtIu3OoE5Q==~3555637~3748404; _gcl_au=1.1.560795829.1693558800; deviceId=623f8bee-ebf1-c86c-65dc-aa056a3cee71; _ga=GA1.1.636144554.1693558800; _ga_SPS4ND2MGC=GS1.1.1693558800.1.0.1693558800.0.0.0; _ym_uid=1693558800995501144; _ym_d=1693558800; _ym_isad=1; _by_l_g_d=584de78c-b7c7-d2c0-6f3a-e7cbbe143525; BYBIT_REG_REF_prod={"lang":"ru-RU","g":"584de78c-b7c7-d2c0-6f3a-e7cbbe143525","medium":"direct","url":"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=64"}; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218a4ff880d4fd8-05bfbc937d5dc3-26031f51-2073600-18a4ff880d5899%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_a_u_v%22%3A%220.0.5%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThhNGZmODgwZDRmZDgtMDViZmJjOTM3ZDVkYzMtMjYwMzFmNTEtMjA3MzYwMC0xOGE0ZmY4ODBkNTg5OSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218a4ff880d4fd8-05bfbc937d5dc3-26031f51-2073600-18a4ff880d5899%22%7D; ak_bmsc=70FC0A382730428AD9B09487F5384F62~000000000000000000000000000000~YAAQj2pkX/nVWEmKAQAAd4j4TxQpdUWOWVJiYvQNgnFQSKekvWIr+DnPz6scmBbXJzAL90Sztl+VLbbQU34BDmDPAlFjs34ZI3KRTBD/eCdfByUV9Vxzxf0bxGhgVo8dgh+BKbD9/cH3WJQ7Bq3mjFR5d0ZhryGH6BSTucdbitwRwf4FytS0RkCUE4/tplBZTePU6c9cvGOA0mpuCNizTIy5EctI1GTaQmQBKJ+2KNXgKoSeISIEIIsfgxZChE9QU4pRK79eIWpgVgvraUjdPn3V1KilwRs9bGWrGNP4lDcdTLOyTdeVMCDTFLVOj+JDAP4zDMoMNw/pok2D9pbPGliTw16H3DA1kMTYfJ60f51SrcOCQdc83VuNvtR0iDer+gS4vp9NDD96eu5P0FsbhiI49Ahc4EkZVs7jbmuemDu2RYQPphHQTL8fD5kOS+ruNuTDE8h+eYITahbthwIBOn8Z7uoKJJMxSV+m8nJJfEMHKRRTJgkhNz6PRQ53W8o=; b_t_c_k=; bm_sv=2D19E595422E9C69D08683472613026F~YAAQj2pkX33eWEmKAQAAcmP5TxRw65uU6WvIXTdhwGvkuYvSg2cOTi6npjFa/Z+yn48h80J5ijV6iy4FqFJbfFGG2oSn+/acYc3I6RGdVJdGy40uoV+KI23bsuYBV4wOL88STthvzr+xr/lual5FfgdgUDevmk6hL+yZ95xqWjPMJzujxZQPIUwuoZDkQ276tmRTjpMqPUnM7M1olJqIp/ab9UM6KZBRQDDgBPp70/cy1BX2MHGA4IVxBM5sdfXq~1',
        'guid': '584de78c-b7c7-d2c0-6f3a-e7cbbe143525',
        'lang': 'ru-RU',
        'origin': 'https://www.bybit.com',
        'platform': 'PC',
        'pragma': 'no-cache',
        'referer': 'https://www.bybit.com/',
        'risktoken': 'v2:gRoGPWGNxuntD529Tq48KdWtwTiruYNJBVd0+26eFFFigi/szs0LteXiAQ/ilywez6X/RKjEcKJ3MoHO3gdO4HvqCuoMiCyt/S+SSNB4GMuqLisq52th8W8xWlPryy0P0Z1E8355QSPc+urs30v7YRFQM+GYCdLLIILjOfLzW2ZBOw+m3YExxzCHbEpKBauXxglC6wYGs+q8QI8Aw6ojApQ7ND2zIMEU+IQX5YKLY+BlpkE=',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'traceparent': '00-219712d855ec3fe8177e870a817c2d1b-4892b5a1de50f165-00',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    json_data = {
        'userId': '',
        'tokenId': 'USDT',
        'currencyId': 'RUB',
        'payment': [
            '64',
        ],
        'side': '1',
        'size': '10',
        'page': '1',
        'amount': '20000',
        'authMaker': False,
        'canTrade': False,
    }

    response = requests.post('https://api2.bybit.com/fiat/otc/item/online', cookies=cookies, headers=headers, json=json_data).json()
    
    price = response['result']['items'][0]['price']
    
    return price


# Часть с запросом по Api Binance
def btc_usdt():
    client = Client(api_key, secret, {"timeout": 40})
    response = client.get_symbol_ticker(symbol="BTCUSDT")
    price = response.get('price')
    return price


if __name__ == '__main__':
    bot.polling(none_stop=True)
