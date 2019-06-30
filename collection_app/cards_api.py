import abc
from functools import lru_cache

import requests


class CardAPI:
    """
    Abstract class to factor multiple card APIs
    Implementations could be HTTPS API, SCRAPING, etc

    """
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def _get_card(cls, name) -> dict:
        """
        Get all card information into a class object
        This class object should then be read and/or returned when requested.
        """

    @classmethod
    @abc.abstractmethod
    def get_card_values(cls, name) -> dict:
        """
        Get card value information
        This class object should then be read and/or returned when requested.
        """

    @classmethod
    @abc.abstractmethod
    def get_card_sets(cls, name) -> list:
        """
        Get all sets in which the card has been printed
        """

    @classmethod
    @abc.abstractmethod
    def validate(cls, name) -> list:
        """
        Validate card existence against external api
        """


class ScryfallAPI(CardAPI):

    """
    Implementation of abstract CardAPI class using ScryfallAPI external API
    Several limitation on the request must be followed. Delay for example.
    """

    REQUEST = {
        'API': 'https://api.scryfall.com',
        'CARDS_ENDPOINT': '/cards/named',
        'DELAY': 0.1,
        'ENCODING': 'utf-8',
        'HEADER_AUTH': {'Authorization': 'Bearer cs{client_secret}'},
        'HEADER_CONTENT': {'Content-Type': 'application/json'},
    }

    def __init__(self):
        super().__init__()

    @classmethod
    @lru_cache(maxsize=10000)
    def _get_card(cls, name) -> dict:
        """
        Using external HTTPS API, get card information

        While the first try attempts to get card info uses the /exact endpoint and is more exact,
        the fuzzy method might help when providing miss-spelled cards.

        :param name: card name
        :return: json with extracted information
        """

        try:
            response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?exact={name}')
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            try:
                response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?fuzzy={name}')
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as err:
                raise err

    @classmethod
    def get_card_values(cls, name) -> dict:
        """
        With all card information from self._ged_card, get the prices vallues and return them
        separated in foil and non-foil

        :param name: string -> card name
        :return: dict -> foil and non-foil keys
        """
        prices = cls._get_card(name=name)['prices']
        return dict({'foil': prices['usd_foil'], 'non-foil': prices['usd']})

    @classmethod
    def get_card_sets(cls, name) -> list:
        """
        Get all sets in which the card has been printed using external Scryfall API

        :param name: string -> card name
        :return: list -> all sets in which the card has been printed
        """

        uri = cls._get_card(name=name)['prints_search_uri']

        try:
            response = requests.get(url=uri)
            response.raise_for_status()
            return [x['set_name'] for x in response.json()['data']]
        except requests.HTTPError as err:
            raise err

    @classmethod
    def validate(cls, name) -> bool:
        """
        Given a card name, check its existence againts external API
        :param name: string -> card name
        :return: bool -> True or false
        """

        try:
            cls._get_card(name=name)
            return True
        except requests.HTTPError:
            return False
