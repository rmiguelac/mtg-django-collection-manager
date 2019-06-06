import pytest
from mock import Mock, patch

from collection_app.cards import Card
from collection_app.cards_api import ScryfallAPI


GOOD_RESPONSE = {'object': 'card', 'id': '6b3a20ac-1860-4513-bb73-35d23b088b04',
                 'oracle_id': 'de2440de-e948-4811-903c-0bbe376ff64d', 'multiverse_ids': [397719],
                 # lots more of info in json
                 'mtgo_id': 57258, 'prices': {'usd': '91.40', 'usd_foil': '111.66', 'eur': '69.87', 'tix': '30.29'}}


@pytest.fixture
def mock_external_api():
    return Mock(spec=ScryfallAPI)


class TestCard:

    def test_card_instantiation_failure(self):

        with patch('collection_app.cards_api.ScryfallAPI.get_card', side_effect=ValueError('Unable')):
            with pytest.raises(ValueError) as excp_info:
                Card(name='Not-a-real-card', external_api=ScryfallAPI)
            assert 'Unable to instantiate' in str(excp_info.value)

    def test_card_instantiation_success(self, mock_external_api):
        card = Card(name='Mox Opal', external_api=mock_external_api)
        mock_external_api.get_card.return_value = GOOD_RESPONSE
        assert isinstance(card, Card)

    def test_card_price_is_float(self,  mock_external_api):
        card = Card(name='Mox Opal', external_api=mock_external_api)
        mock_external_api.get_card.return_value = GOOD_RESPONSE
        assert isinstance(card.value, float)

    def test_card_foil_price(self, mock_external_api):
        card = Card(name='Mox Opal', foil=True, external_api=mock_external_api)
        mock_external_api.get_card.return_value = GOOD_RESPONSE
        assert card.value == 111.66

    def test_card_non_foil_price(self, mock_external_api):
        card = Card(name='Mox Opal', foil=False, external_api=mock_external_api)
        mock_external_api.get_card.return_value = GOOD_RESPONSE
        assert card.value == 91.40
