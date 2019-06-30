import pytest
from unittest.mock import MagicMock, patch

from requests import HTTPError

from collection_app.cards import Card
from collection_app.cards_api import ScryfallAPI
from collection_app.tests import constants


@pytest.fixture
def mock_external_api():
    card_api_instance = MagicMock(spec=ScryfallAPI)
    card_api_instance.get_card_values.return_value = dict(
        {'foil': constants.GOOD_RESPONSE['prices']['usd_foil'],
         'non-foil': constants.GOOD_RESPONSE['prices']['usd']})
    return card_api_instance


class TestCard:

    def test_card_instantiation(self, mock_external_api):
        card = Card(name='Mox Opal', card_api=mock_external_api)
        assert isinstance(card, Card)

    def test_card_is_valid(self, mock_external_api):
        card = Card(name='Mox Opal', card_api=mock_external_api)
        assert card.is_valid is True

    def test_card_is_invalid(self, mock_external_api):
        mock_external_api.get_card_values.side_effect = HTTPError
        card = Card(name='Mx Ol', card_api=mock_external_api)
        assert card.is_valid is False

    def test_card_value_is_float(self, mock_external_api):
        card = Card(name='Mox Opal', card_api=mock_external_api)
        assert isinstance(card.value, float)

    def test_card_foil_value(self, mock_external_api):
        card = Card(name='Mox Opal', foil=True, card_api=mock_external_api)
        assert card.value == 111.66

    def test_card_non_foil_value(self, mock_external_api):
        card = Card(name='Mox Opal', foil=False, card_api=mock_external_api)
        assert card.value == 91.40
