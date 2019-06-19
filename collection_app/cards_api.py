import logging
import abc

import requests


logger = logging.getLogger(__name__)


class CardAPI:
    """
    Abstract class to factor multiple card APIs
    Implementations could be HTTPS API, SCRAPING, etc

    """
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def _get_card(cls, name):
        """
        Get all card information into a class object
        This class object should then be read and/or returned when requested.
        """

    @classmethod
    @abc.abstractmethod
    def get_card_values(cls, name):
        """
        Get card value information
        This class object should then be read and/or returned when requested.
        """


class ScryfallAPI(CardAPI):

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
        except requests.HTTPError as err:
            logger.debug(f'Card "{name}" not found. trying fuzzy match. Response: {err}')
            try:
                response = requests.get(url=f'{cls.REQUEST["API"]}{cls.REQUEST["CARDS_ENDPOINT"]}?fuzzy={name}')
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as err:
                logger.debug(f'Card "{name}" not found. Response: {err}')
                raise ValueError

    @classmethod
    def get_card_values(cls, name):
        prices = cls._get_card(name=name)['prices']
        return dict({'foil': prices['usd_foil'], 'non-foil': prices['usd']})

