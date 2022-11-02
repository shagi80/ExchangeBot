import requests
import json


class APIException(Exception):

    def __init__(self, message: str = None):
        self.message = message

    def __str__(self):
        return self.message if self.message else 'Ошибка при обращении к обменнику.'


class APIManager:
    APILAYER_URL = "https://api.apilayer.com/exchangerates_data/"
    APILAYER_KEY = {
        "apikey": '15abCIi3YjwUHDdaZvLBV3lVARLR8C56'
    }

    @staticmethod
    def get_symbols() -> dict:
        request_string = f'{APIManager.APILAYER_URL}symbols'
        response = requests.request("GET", request_string, headers=APIManager.APILAYER_KEY)
        status_code = response.status_code
        if status_code != 200:
            raise APIException()
        result = json.loads(response.text)
        if result['success']:
            return result['symbols']
        else:
            raise APIException('Обменик отказал в предоставлении данных.')

    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        request_string = f'{APIManager.APILAYER_URL}convert?to={quote}&from={base}&amount={amount}'
        response = requests.request("GET", request_string, headers=APIManager.APILAYER_KEY)
        status_code = response.status_code
        if status_code != 200:
            raise APIException()
        result = json.loads(response.text)
        if result['success']:
            return result['result']
        else:
            raise APIException('Обменник отказал в конвертации.')


