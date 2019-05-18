from bs4 import BeautifulSoup
import requests
from requests import HTTPError


class CardPricer:

    def __init__(self, name, set_name=None, condition=None):
        self.name = name
        self.set_name = set_name
        self.condition = condition

    def __repr__(self):
        return f'Card(name={self.name}, set_name={self.set_name}, condition={self.condition})'

    def __str__(self):
        return f'Card named {self.name} from {self.set_name} set_name in {self.condition} condition'

    @property
    def price(self):
        try:
            price_url = 'https://www.ligamagic.com.br/?view=cards/card&card='
            response = requests.get(url=f'{price_url}{self.name}')
            soup = BeautifulSoup(response.text, 'html.parser')
            price = soup.find('div', id='precos-menor')
            if not price:
                raise ValueError
            response.raise_for_status()
            return float(price.text.split(' ')[1])
        except HTTPError as herr:
            print(herr)
        except ValueError as verr:
            print(f'Card {self.name} not found!')

