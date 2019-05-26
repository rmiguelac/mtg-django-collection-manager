from bs4 import BeautifulSoup
import requests
from requests import HTTPError


CARD_ENDPOINT = '?view=cards/card&card='
SCRAP_WEBSITE = 'https://www.ligamagic.com.br'


def get_crawl_delay():

    try:
        robots = requests.get(url=f'{SCRAP_WEBSITE}/robots.txt').text
        for block in robots.split('\r\n\r\n'):
            if 'User-agent: *' in block:
                for line in block.split('\r\n'):
                    if 'delay' in line:
                        return line.split(' ')[1]
    except requests.HTTPError:
        return 'Unable to process robots.txt'


class CardPricer:
    '''
    Fetch card price considering name, set and condition
    '''

    def __init__(self, name, set=None, condition=None):
        self.name = name
        self.set= set
        self.condition = condition

    def __repr__(self):
        return f'Card(name={self.name}, set_name={self.set}, condition={self.condition})'

    def __str__(self):
        return f'Card named {self.name} from {self.set} set_name in {self.condition} condition'

    @property
    def price(self):
        try:
            price_url = f'{SCRAP_WEBSITE}/{CARD_ENDPOINT}'
            response = requests.get(url=f'{price_url}{self.name}')
            soup = BeautifulSoup(response.text, 'lxml')
            price = soup.find('div', id='card-alerta').find('div', class_='preco-menor').text
            if not price:
                raise ValueError
            response.raise_for_status()
            return price.split(' ')[1]
        except HTTPError as herr:
            print(herr)
        except ValueError:
            print(f'Card {self.name} not found!')
