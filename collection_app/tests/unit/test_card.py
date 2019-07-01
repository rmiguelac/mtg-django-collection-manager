from unittest.mock import patch

from requests import HTTPError

from collection_app.cards import CardScryfallImpl
from collection_app.tests import constants


class TestCard:

    def test_card_instantiation(self):
        card = CardScryfallImpl(name='Mox Opal')
        assert isinstance(card, CardScryfallImpl)

    def test_card_is_valid(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            card = CardScryfallImpl(name='Mox Opal')
            assert card.is_valid is True

    def test_card_is_invalid(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            card = CardScryfallImpl(name='Mx Ol')
            assert card.is_valid is False

    def test_card_value_is_float(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            card = CardScryfallImpl(name='Mox Opal')
            assert isinstance(card.value, float)

    def test_card_foil_value(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            card = CardScryfallImpl(name='Mox Opal', foil=True)
            assert card.value == 114.35

    def test_card_non_foil_value(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            card = CardScryfallImpl(name='Mox Opal', foil=False)
            assert card.value == 91.44
