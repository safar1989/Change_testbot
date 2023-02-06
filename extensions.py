import requests
import json
from config import keys


class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise ApiException(f'Невозможно перевести одинаковые валюты! {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту! {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту! {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество! {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]]
        return total_quote