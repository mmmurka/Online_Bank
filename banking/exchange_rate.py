import requests


def get_exchange_rate():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        uah_to_usd_rate = result[0]['rateSell']
        uah_to_eur_rate = result[1]['rateSell']
        return uah_to_usd_rate, uah_to_eur_rate
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

