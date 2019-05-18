import mtgsdk
from functools import lru_cache

@lru_cache()
def validate(card_name, card_set_name):
    """Validate card agains mtgsdk"""

    card = mtgsdk.Card.where(name=card_name).where(set_name=card_set_name).all()

    if card:
        return True

    return False
