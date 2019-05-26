from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag
import pandas as pd
import re
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


class Currency:

    @classmethod
    def get_general_format(cls, value):
        if not isinstance(value, str):
            return str(value).replace('.', '').replace(',', '.')
        else:
            return value.replace('.', '').replace(',', '.')


class CardPricer:
    '''
    Fetch card price considering name, set and condition
    '''

    def __init__(self, name, card_set=None, condition=None):
        self.name = name
        self.card_set = card_set
        self.condition = condition

    def __repr__(self):
        return f'Card(name={self.name}, card_set={self.card_set}, condition={self.condition})'

    def __str__(self):
        return f'Card named {self.name} from {self.card_set} card_set in {self.condition} condition'

    @property
    def price(self):
        return self._get_price()

    def _get_soup_from_uri(self, uri):
        response = requests.get(url=uri)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def _scrap_child_website(self, uri):
        soup = self._get_soup_from_uri(uri=uri)
        prices_table = soup.find('div', class_='itemMain').find_all('table')[-1].prettify()
        card_sets = pd.Series([x['title'] for x in soup.find_all('img', class_='icon-edicao')])
        raw_table = pd.read_html(prices_table, header=0)
        table = [x.loc[:, ~x.columns.str.contains('^Unnamed')].drop(axis=1, labels=['Idioma', 'Estoque']) for x in raw_table]
        table[0]['Edição'] = table[0]['Edição'].astype(str)
        for cs, (index, row) in zip(card_sets, table[0].iterrows()):
            row['Edição'] = re.sub('nan', cs, row['Edição'])
            row['Qualidade'] = row['Qualidade']
            if self.condition in row['Qualidade']:
                if row['Edição'] == self.card_set:
                    return row['Preço']

    def _get_price(self):
        try:
            price_url = f'{SCRAP_WEBSITE}/{CARD_ENDPOINT}{self.name}'
            soup = self._get_soup_from_uri(uri=price_url)
            stores = soup.find_all('div', class_='estoque-linha')
            for offer in stores:
                if isinstance(offer, Tag):
                    o_card_set = offer.find('div', class_='e-col2').text
                    o_card_condition = re.sub('\s', '', offer.find('div', class_='e-col4').text)
                    if re.match(self.card_set, o_card_set, re.IGNORECASE) and re.match(self.condition, o_card_condition, re.IGNORECASE):
                        cprice = Currency.get_general_format(offer.find('div', class_='e-col3').text.split(' ')[-1])
                        try:
                            o_card_price = float(cprice)
                        except ValueError:
                            o_card_shop = offer.find('div', class_='e-col8')
                            o_card_shop_uri = o_card_shop.a['href']
                            if re.match(self.condition, o_card_condition, re.IGNORECASE):
                                return self._scrap_child_website(f'{SCRAP_WEBSITE}/{o_card_shop_uri}')
                        else:
                            return o_card_price
        except HTTPError as herr:
            print(herr)

cp = CardPricer(name='Mox Opal', card_set='Cicatrizes de Mirrodin', condition='NM').price
print(cp)
