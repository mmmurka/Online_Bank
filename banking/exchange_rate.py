# get_exchange_rate.py
import requests
from datetime import timedelta
from django.core.cache import cache

def get_exchange_rate():
    # Пытаемся получить данные из кеша
    cached_data = cache.get('exchange_rate')

    if cached_data:
        return cached_data

    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        uah_to_usd_rate = result[0]['rateSell']
        uah_to_eur_rate = result[1]['rateSell']

        # Сохраняем данные в кеше
        cache.set('exchange_rate', (uah_to_usd_rate, uah_to_eur_rate), 5 * 60)  # 5 минут
        return uah_to_usd_rate, uah_to_eur_rate
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
