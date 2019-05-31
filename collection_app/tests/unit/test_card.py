import pytest

from collection_app.cards import Card


class TestCard:

    def test_card_existence_failure(self):
        with pytest.raises(ValueError) as excp_info:
            Card(name='Blip blop')
        assert 'Unable to instantiate' in str(excp_info.value)

    def test_card_existence_success(self):
        card = Card(name='Mox Opal')
        assert isinstance(card, Card)

    def test_card_price_is_float(self):
        card = Card(name='Mox Opal')
        assert isinstance(card.price, float)

