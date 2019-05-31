import pytest

from collection_app.cards import Card


class TestCard:

    def test_card_price_is_float(self):
        card = Card(name='Mox Opal')
        assert isinstance(card.price, float)

    def test_card_existence_failure(self):
        pass

    def test_card_existence_success(self):
        pass
