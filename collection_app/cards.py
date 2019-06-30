from requests import HTTPError

import collection_app.cards_api as ext_apis


class Card:

    def __init__(self, name, expansion=None, condition=None, foil=None, card_api=None):
        """
        A class to be used as validator and information fetcher

        :param name: Card name
        :param expansion: Set in which card was printed
        :param condition: One of NM, SP, MP, HP, D
        :param foil: bool with either True or False
        :param card_api: class to provide information about the card. Use of dependency injection
        """
        self.name = name
        self.expansion = expansion
        self.condition = condition
        self.foil = foil
        self._value = None
        self._sets = None
        self._is_valid = False
        self._card_api = card_api

    @property
    def sets(self) -> list:
        """
        Sets/Expansions in which the card have been printed
        :return: list with all given sets in english
        """

        return self.sets

    @sets.setter
    def sets(self, new_value) -> None:
        self._sets = new_value

    @sets.getter
    def sets(self) -> list:
        sets = self._card_api.get_card_sets(name=self.name)
        self.sets = sets
        return sets

    @property
    def value(self) -> float:
        """
        Card value in USD

        :return: return float object which represents the card price
        """
        return self.value

    @value.getter
    def value(self) -> float:
        price = self._card_api.get_card_values(name=self.name)

        if self.foil:
            self.value = price['foil']
            return float(self._value)
        else:
            self.value = price['non-foil']
            return float(self._value)

    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value

    @property
    def is_valid(self) -> bool:
        """
        Check card existence against external API

        :return: True if able to find it in external API, False otherwise
        """
        return self.is_valid

    @is_valid.getter
    def is_valid(self) -> bool:
        """
        Validate card existence given its name using external API
        :return: bool -> either True or False
        """

        self.is_valid = self._card_api.validate(name=self.name)
        return self._is_valid

    @is_valid.setter
    def is_valid(self, new_value) -> None:
        self._is_valid = new_value


class CardScryfallImpl(Card):

    def __init__(self, name, expansion=None, condition=None, foil=False, card_api=ext_apis.ScryfallAPI):
        super().__init__(name, expansion, condition, foil, card_api=card_api)
