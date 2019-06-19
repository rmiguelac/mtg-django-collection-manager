import logging

from collection_app.cards_api import ScryfallAPI


logger = logging.getLogger(__name__)


class Card:

    def __init__(self, name, set_name=None, condition=None, foil=None, card_api=None):
        """
        A class to be used as validator and information fetcher

        :param name: Card name
        :param set_name: Set in which card was printed
        :param condition: One of NM, SP, MP, HP, D
        :param foil: bool with either True or False
        :param card_api: class to provide information about the card. Use of dependency injection
        """
        self.name = name
        self.set_name = set_name
        self.condition = condition
        self.foil = foil
        self._value = None
        self._card_api = card_api

    @property
    def value(self):
        """
        Card value in USD

        :return: return float object which represents the card price
        """
        return float(self.value)

    @value.getter
    def value(self):
        price = self._card_api.get_card_values(name=self.name)
        print(type(price))

        if self.foil:
            self.value = price['foil']
            return float(self._value)
        else:
            self.value = price['non-foil']
            return float(self._value)

    @value.setter
    def value(self, new_value):
        self._value = new_value
