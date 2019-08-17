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
            card = CardScryfallImpl(name='Mox Opal', expansion='Scars of Mirrodin')
            assert card.is_valid is True

    def test_card_is_invalid(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            card = CardScryfallImpl(name='Mx Ol', expansion='Scars of Mirrodin')
            assert card.is_valid is False

    def test_card_value_is_float(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            card = CardScryfallImpl(name='Mox Opal', expansion='Scars of Mirrodin')
            assert isinstance(card.value, float)

    def test_card_value_is_null(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.NULL_PRICE_RESPONSE):
                card = CardScryfallImpl(name='Mox Opal', expansion='Scars of Mirrodin')
                assert card.value == 0.00

    def test_card_foil_value(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                card = CardScryfallImpl(name='Mox Opal', foil=True, expansion='Scars of Mirrodin')
                assert card.value == 196.98

    def test_card_non_foil_value(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                card = CardScryfallImpl(name='Mox Opal', foil=False, expansion='Scars of Mirrodin')
                assert card.value == 96.37

    def test_card_value_by_set(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                card = CardScryfallImpl(name='Mox Opal', foil=False, expansion='Scars of Mirrodin')
                assert card.value == 96.37
                card = CardScryfallImpl(name='Mox Opal', foil=False, expansion='Modern Masters 2015')
                assert card.value == 97.98
                card = CardScryfallImpl(name='Mox Opal', foil=True, expansion='Kaladesh Inventions')
                assert card.value == 302.34
