import logging

import requests


logger = logging.getLogger(__name__)

REQUEST = {
    'API': 'https://api.scryfall.com',
    'CARDS_ENDPOINT': '/cards/named',
    'DELAY': 0.1,
    'ENCODING': 'utf-8',
    'HEADER_AUTH': {'Authorization': 'Bearer cs{client_secret}'},
    'HEADER_CONTENT': {'Content-Type': 'application/json'},
}


def get_card(name):
    """
    Using external HTTPS API, get card information
    :param name: card name
    :return: json with extracted information
    """

    try:
        response = requests.get(url=f'{REQUEST["API"]}{REQUEST["CARDS_ENDPOINT"]}?exact={name}')
        response.raise_for_status()
        print(response.text)
        print(response.status_code)
        return response.json()
    except requests.HTTPError as err:
        logger.debug(f'Card "{name}" not found. trying fuzzy match. Response: {err}')
        try:
            response = requests.get(url=f'{REQUEST["API"]}{REQUEST["CARDS_ENDPOINT"]}?fuzzy={name}')
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
            cls._get_existence(*args, **kwargs)
            return super(Card, cls).__new__(cls)
        except ValueError:
            raise ValueError(f'Unable to instantiate Card with current value as it is not a valid card')

    def __init__(self, name, set_name=None, condition=None, foil=None):
        """
        A class to be used as validator and information fetcher
        :param name:
        :param set_name:
        :param condition:
        :param foil:
        """
        self.name = name
        self.set_name = set_name
        self.condition = condition
        self.foil = foil

    @property
    def price(self):
        """
        Card price in USD
        :return: return float object which represents the card price
        """
        return self._get_price()

    def _get_price(self):
        """
        Making use of external API, get daily updated USD card price
        :return: string with price
        """
        if self.foil:
            return float(get_card(name=self.name)['prices']['usd_foil'])
        else:
            return float(get_card(name=self.name)['prices']['usd'])

    @classmethod
    def _get_existence(cls, name):
        return get_card(name=name)

    def __repr__(self):
        return f'{self.__class__, self.__dict__}'

    def __str__(self):
        return f'{__class__.__name__}(name={self.name}, set_name={self.set_name}, condition={self.condition}, foil={self.foil})'
