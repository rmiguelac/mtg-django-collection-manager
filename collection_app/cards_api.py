import abc
from functools import lru_cache
import logging
from typing import List, Dict

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CardAPI:
    """
    Abstract class to factor multiple card APIs
    Implementations could be HTTPS API, SCRAPING, etc

    """
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def _get_card(cls, name: str) -> Dict:
        """
        Get all card information into a class object
        This class object should then be read and/or returned when requested.
        """

    @classmethod
    @abc.abstractmethod
    def get_card_values(cls, name: str) -> Dict:
        """
        Get card value information
        This class object should then be read and/or returned when requested.
        """

    @classmethod
    @abc.abstractmethod
    def get_card_sets(cls, name: str) -> List:
        """
        Get all sets in which the card has been printed
        """

    @classmethod
    @abc.abstractmethod
    def validate(cls, name: str, expansion: str) -> List:
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
    def _get_card(cls, name: str) -> Dict:
        """
        Using external HTTPS API, get card information

        While the first try attempts to get card info uses the /exact endpoint and is more exact,
        the fuzzy method might help when providing miss-spelled cards.
        """

        try:
            logger.info(f'About to request for {name} card')
            response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?exact={name}')
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            try:
                logger.info(f'Unable to locate exactly {name} named card, looking into fuzzy naming...')
                response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?fuzzy={name}')
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as err:
                raise err

    @classmethod
    def get_card_values(cls, name: str) -> Dict:
        """
        With all card information from self._ged_card, get the prices vallues and return them
        separated in foil and non-foil
        """
        logger.info('Getting card values')
        prices = cls._get_card(name=name)['prices']
        logger.debug(f'Card values are {prices}')
        return dict({'foil': prices['usd_foil'], 'non-foil': prices['usd']})

    @classmethod
    def get_card_sets(cls, name: str) -> List:
        """
        Get all sets in which the card has been printed using external Scryfall API
        """

        uri = cls._get_card(name=name)['prints_search_uri']

        try:
            logger.info(f'Fetching sets in which {name} was printed...')
            response = requests.get(url=uri)
            response.raise_for_status()
            return [x['set_name'] for x in response.json()['data']]
        except requests.HTTPError as err:
            logger.error(err)
            raise err

    @classmethod
    def validate(cls, name: str, expansion: str) -> bool:
        """
        Given a card name, check its existence againts external API
        """

        try:
            logger.info(f'Validating card {name} existence against external API...')
            cls._get_card(name=name)
        except requests.HTTPError:
            logger.error(f'There is no such card named {name}!')
            return False

        try:
            logger.info(f'Validating card {name} existence in expansion set {expansion}')
            sets = cls.get_card_sets(name=name)
            if expansion in sets:
                logger.debug(f'{expansion} found in {sets}')
                return True
            else:
                logger.error(f'{expansion} not found in {sets}')
                return False
        except requests.HTTPError:
            logger.error(f'There is not such card {name} in expansion set {expansion}')
            return False
