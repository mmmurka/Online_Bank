import requests
import logging
from django.core.cache import cache

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_exchange_rate():
    try:
        # Пытаемся получить данные из кеша
        cached_data = cache.get('exchange_rate')

        if cached_data:
            return cached_data

        else:
            url = 'https://api.monobank.ua/bank/currency'
            response = requests.get(url)

            if response.status_code == 200:
                result = response.json()
                uah_to_usd_rate = result[0]['rateSell']
                uah_to_eur_rate = result[1]['rateSell']

                # Сохраняем данные в кеше
                cache.set('exchange_rate', (uah_to_usd_rate, uah_to_eur_rate), 5 * 60)  # 5 минут
                logger.info(f"Data saved in cache: USD {uah_to_usd_rate}, EUR {uah_to_eur_rate}")
                return uah_to_usd_rate, uah_to_eur_rate
            else:
                logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                uah_to_usd_rate = 0.00
                uah_to_eur_rate = 0.00
                return uah_to_usd_rate, uah_to_eur_rate

    except Exception as e:
        logger.error(f"Failed to fetch data. Error: {e}")


