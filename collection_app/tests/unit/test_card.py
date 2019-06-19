import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock, create_autospec

from collection_app.cards import Card
from collection_app.cards_api import ScryfallAPI


GOOD_RESPONSE = {'object': 'card', 'id': '6b3a20ac-1860-4513-bb73-35d23b088b04', 'name': 'Mox Opal',
                 'oracle_id': 'de2440de-e948-4811-903c-0bbe376ff64d', 'multiverse_ids': [397719],
                 # lots more of info in json
                 'mtgo_id': 57258, 'prices': {'usd': '91.40', 'usd_foil': '111.66', 'eur': '69.87', 'tix': '30.29'}}


@pytest.fixture
def mock_external_api():
    card_api_instance = MagicMock(spec=ScryfallAPI)
    card_api_instance.get_card_values.return_value = dict(
        {'foil': GOOD_RESPONSE['prices']['usd_foil'],
         'non-foil': GOOD_RESPONSE['prices']['usd']})
    return card_api_instance


class TestCard:

    def test_card_instantiation_success(self, mock_external_api):
        card = Card(name='Mox Opal', card_api=mock_external_api)
        assert isinstance(card, Card)

    def test_card_price_is_float(self, mock_external_api):
        card = Card(name='mox opal', card_api=mock_external_api)
        assert isinstance(card.value, float)

    def test_card_foil_price(self, mock_external_api):
        card = Card(name='Mox Opal', foil=True, card_api=mock_external_api)
        assert card.value == 111.66

    def test_card_non_foil_price(self, mock_external_api):
        card = Card(name='Mox Opal', foil=False, card_api=mock_external_api)
        assert card.value == 91.40
