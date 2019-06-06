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

    @abc.abstractmethod
    def __init__(self, name):
        self.name = name
        self._value = None

    @classmethod
    @abc.abstractmethod
    def get_card(cls, name):
        """
        Get all card information into a class object
        This class object should then be read and/or returned when requested.
        """

    @property
    @abc.abstractmethod
    def value(self):
        """
        Return a dict with both foil and non-foil price
        """

    @value.setter
    @abc.abstractmethod
    def value(self, new_value):
        pass

    @value.getter
    @abc.abstractmethod
    def value(self):
        pass


class ScryfallAPI(CardAPI):

    REQUEST = {
        'API': 'https://api.scryfall.com',
        'CARDS_ENDPOINT': '/cards/named',
        'DELAY': 0.1,
        'ENCODING': 'utf-8',
        'HEADER_AUTH': {'Authorization': 'Bearer cs{client_secret}'},
        'HEADER_CONTENT': {'Content-Type': 'application/json'},
    }

    def __init__(self, name):
        super().__init__(self)
        self.name = name
        self._value = None

    @classmethod
    def get_card(cls, name):
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

    @property
    def value(self):
        return self._value

    @value.getter
    def value(self):
        prices = self.get_card(name=self.name)['prices']
        self.value = dict({'foil': prices['usd_foil'], 'non-foil': prices['usd']})
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
