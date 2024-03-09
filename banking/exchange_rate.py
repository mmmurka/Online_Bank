from django.core.cache import cache
import datetime
from django.conf import settings
import requests


def get_exchange_rate():
    # Попытка получить данные из кеша
    cached_data = cache.get('exchange_rate_data')
    if cached_data:
        uah_to_usd_rate, uah_to_eur_rate, timestamp = cached_data
        # Проверка, актуальны ли данные в кеше
        current_time = datetime.datetime.now(datetime.timezone.utc)
        expiration_time = timestamp + datetime.timedelta(minutes=settings.CACHE_TIMEOUT)
        if current_time <= expiration_time:
            return uah_to_usd_rate, uah_to_eur_rate

    # Если данные в кеше устарели или отсутствуют, делаем запрос к API
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        uah_to_usd_rate = result[0]['rateSell']
        uah_to_eur_rate = result[1]['rateSell']
        timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
        # Обновляем кеш с новыми данными
        cache.set('exchange_rate_data', (uah_to_usd_rate, uah_to_eur_rate, timestamp))
        return uah_to_usd_rate, uah_to_eur_rate
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")