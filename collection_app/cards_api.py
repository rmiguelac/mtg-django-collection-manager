import abc
from functools import lru_cache
import logging
from typing import List, Dict
from time import sleep

import requests

logger = logging.getLogger(__name__)


class CardAPI:
    """
    Abstract class to factor multiple card APIs
    Implementations could be HTTPS API, SCRAPING, etc

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.card = None

    @abc.abstractmethod
    def _get_card(self, name: str) -> Dict:
        """
        Get all card information into a class object
        This class object should then be read and/or returned when requested.
        """

    @abc.abstractmethod
    def get_card_values(self, name: str, expansion: str) -> Dict:
        """
        Get card value information
        This class object should then be read and/or returned when requested.
        """

    @abc.abstractmethod
    def get_card_sets(self, name: str) -> List:
        """
        Get all sets in which the card has been printed
        """

    @abc.abstractmethod
    def validate(self, name: str, expansion: str) -> List:
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
        self.card = None

    @lru_cache(maxsize=10000)
    def _get_card(self, name: str, method: str = 'exact') -> Dict:
        """
        Using external HTTPS API, get card information

        While the first try attempts to get card info uses the /exact endpoint and is more exact,
        the fuzzy method might help when providing miss-spelled cards.
        """

        if not self.card:
            sleep(self.REQUEST['DELAY'])
            try:
                logger.info(f'About to request for {name} card')
                card = requests.get(url=f'{self.REQUEST["API"]}{self.REQUEST["CARDS_ENDPOINT"]}?{method}={name}')
                card.raise_for_status()
                card_info_url = card.json()['prints_search_uri']
                card_info = requests.get(url=card_info_url)
                card_info.raise_for_status()
                self.card = card_info.json()['data']
                return self.card
            except requests.HTTPError:
                try:
                    logger.info(f'Unable to locate exactly {name} named card, looking into fuzzy naming...')
                    self._get_card(name=name, method='fuzzy')
                except requests.HTTPError as err:
                    raise err
        else:
            return self.card

    def get_card_values(self, name: str, expansion: str) -> Dict:
        """
        With all card information from self._get_card, get the values and return them
        separated in foil and non-foil
        """

        prices = {'foil': None, 'non-foil': None}

        logger.info('Getting card values')
        for set_info in self._get_card(name=name):
            if set_info['set_name'] == expansion:
                prices = {
                    'foil': set_info['prices']['usd_foil'],
                    'non-foil': set_info['prices']['usd'],
                }
                logger.debug(f'Card values are {prices}')
                return prices
        return prices

    def get_card_sets(self, name: str) -> List:
        """
        Get all sets in which the card has been printed using external Scryfall API
        """
        card = self._get_card(name=name)
        return [expansion['set_name'] for expansion in card]

    def validate(self, name: str, expansion: str) -> bool:
        """
        Given a card name, check its existence againts external API
        """

        try:
            logger.info(f'Validating card {name} existence against external API...')
            self._get_card(name=name)
        except requests.HTTPError:
            logger.error(f'There is no such card named {name}!')
            return False

        try:
            logger.info(f'Validating card {name} existence in expansion set {expansion}')
            sets = self.get_card_sets(name=name)
            if expansion in sets:
                logger.debug(f'{expansion} found in {sets}')
                return True
            else:
                logger.error(f'{expansion} not found in {sets}')
                return False
        except requests.HTTPError:
            logger.error(f'There is not such card {name} in expansion set {expansion}')
            return False
