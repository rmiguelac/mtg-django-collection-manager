import logging


logger = logging.getLogger(__name__)


class Card:

    def __new__(cls, *args, **kwargs):
        """
        Guarantee that the object being instantiated exists

        :param args: might receive name, set_name, condition and foil
        :param kwargs: might receive name, set_name, condition and foil
        :return: Card cls object if valid object, raise ValueError otherwise
        """
        try:
            kwargs['external_api'].get_card(name=kwargs['name'])
            return super(Card, cls).__new__(cls)
        except ValueError:
            raise ValueError('Unable to instantiate Card with current value as it is not a valid card')

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
        self._value = None
        self._external_api = external_api

    @property
    def value(self):
        """
        Card value in USD

        :return: return float object which represents the card price
        """
        return float(self._value)

    @value.getter
    def value(self):
        """
        Card value in USD

        :return: return float object which represents the card price
        """
        card = self._external_api(name=self.name)
        price = card.value

        if self.foil:
            self.value = price['foil']
            return self._value
        else:
            self.value = price['non-foil']
            return self._value

    @value.setter
    def value(self, new_value):
        """
        Only defined to be used by the getter

        :param new_value: dict with foil and non-foil keys
        """
        self._value = new_value

    def __repr__(self):
        return f'{self.__class__, self.__dict__}'

    def __str__(self):
        return f'{__class__.__name__}(name={self.name}, set_name={self.set_name}, condition={self.condition}, foil={self.foil})'
