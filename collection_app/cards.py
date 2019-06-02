import logging

import requests


logger = logging.getLogger(__name__)


class ScryfallAPI:

    REQUEST = {
        'API': 'https://api.scryfall.com',
        'CARDS_ENDPOINT': '/cards/named',
        'DELAY': 0.1,
        'ENCODING': 'utf-8',
        'HEADER_AUTH': {'Authorization': 'Bearer cs{client_secret}'},
        'HEADER_CONTENT': {'Content-Type': 'application/json'},
    }

    @classmethod
    def get_card(cls, name):
        """
        Using external HTTPS API, get card information

        While the first try to get card info uses the /exact endpoint and may be more exact,
        the fuzzy method might help when providing miss-spelled cards.

        :param name: card name
        :return: json with extracted information
        """

        try:
            response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?exact={name}')
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as err:
            logger.debug(f'Card "{name}" not found. trying fuzzy match. Response: {err}')
            try:
                response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?fuzzy={name}')
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as err:
                logger.debug(f'Card "{name}" not found. Response: {err}')
                raise ValueError


class Card:

    def __new__(cls, *args, **kwargs):
        """
        Guarantee that the object being instantiated exists

        :param args: might receive name, set_name, condition and foil
        :param kwargs: might receive name, set_name, condition and foil
        :return: Card cls object if valid object, raise ValueError otherwise
        """
        try:
            ext_api = kwargs['external_api']
            ext_api.get_card(name=kwargs['name'])
            return super(Card, cls).__new__(cls)
        except ValueError:
            raise ValueError(f'Unable to instantiate Card with current value as it is not a valid card')

    def __init__(self, name, set_name=None, condition=None, foil=None, external_api=None):
        """
        A class to be used as validator and information fetcher

        :param name: Card name
        :param set_name: Set in which card was printed
        :param condition: One of NM, SP, MP, HP, D
        :param foil: bool with either True or False
        :param external_api: class to provide information about the card. Use of dependency injection
        """
        self.name = name
        self.set_name = set_name
        self.condition = condition
        self.foil = foil
        self._price = None
        self._external_api = external_api

    @property
    def price(self):
        """
        Card price in USD

        :return: return float object which represents the card price
        """
        return self._price

    @price.getter
    def price(self):
        """
        Making use of external API, get daily updated USD card price

        :return: string with price
        """
        if self.foil:
            self._price = float(self._external_api.get_card(name=self.name)['prices']['usd_foil'])
            return self._price
        else:
            self._price = float(self._external_api.get_card(name=self.name)['prices']['usd'])
            return self._price

    def __repr__(self):
        return f'{self.__class__, self.__dict__}'

    def __str__(self):
        return f'{__class__.__name__}(name={self.name}, set_name={self.set_name}, condition={self.condition}, foil={self.foil})'


c = Card(name='Mox Opal', external_api=ScryfallAPI()).price
print(c)
