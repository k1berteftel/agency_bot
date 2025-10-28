import random
import uuid
import asyncio
import hashlib
from aiohttp import ClientSession

from config_data.config import Config, load_config


config: Config = load_config()

pass_1 = 'wF5oU3t0UnK12cLTyJIL'
pass_2 = 'TCqWM88am5wqU3kmEi1V'


async def _get_usdt_rub() -> float:
    url = 'https://open.er-api.com/v6/latest/USD'
    async with ClientSession() as session:
        async with session.get(url, ssl=False) as res:
            data = await res.json()
            rub = data['rates']['RUB']
    return float(rub)


def _calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


async def get_robokassa_url(amount: int):
    url = 'https://services.robokassa.ru/InvoiceServiceWebApi/api/CreateInvoice'
    headers = {
        "typ": "JWT",
        "alg": "MD5"
    }
    data = {
        'MerchantLogin': 'Islamsuleyman',
        'OutSum': float(amount),
        'InvoiceType': 'OneTime',
        'MerchantComments': 'Покупка подписки',
        'IsTest': 1
        #'InvId': random.randint(1, 9999999999),
    }
    data['SignatureValue'] = _calculate_signature(*list(data.values()), pass_1)

    async with ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as res:
            if res.status not in [200, 201]:
                print(await res.text())
            data = await res.json()
            print(data)


#asyncio.run(get_robokassa_url(100))


async def check_robokassa_url():
    pass

