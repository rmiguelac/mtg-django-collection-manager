
GOOD_RESPONSE = {"object": "card",
                 "name": "Mox Opal",
                 "uri": "https://api.scryfall.com/cards/6b3a20ac-1860-4513-bb73-35d23b088b04",
                 "scryfall_uri": "https://scryfall.com/card/mm2/223/mox-opal?utm_source=api",
                 "foil": True,
                 "set": "mm2",
                 "set_name": "Modern Masters 2015",
                 "set_type": "masters",
                 "set_uri": "https://api.scryfall.com/sets/28cac015-43df-4e88-90d0-95dcdd894834",
                 "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Amm2&unique=prints",
                 "scryfall_set_uri": "https://scryfall.com/sets/mm2?utm_source=api",
                 "rulings_uri": "https://api.scryfall.com/cards/6b3a20ac-1860-4513-bb73-35d23b088b04/rulings",
                 "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3Ade2440de-e948-4811-903c-0bbe376ff64d&unique=prints",
                 "flavor_text": "The suns of Mirrodin have shone upon perfection only once.",
                 "artist": "Volkan Baǵa",
                 "border_color": "black",
                 "prices": {"usd": "91.44",
                 "usd_foil": "114.35",
                 "eur": "70.51",
                 "tix": "39.21"},
                 "related_uris": {"gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=397719",
                 "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Mox+Opal&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                 "edhrec": "http://edhrec.com/route/?cc=Mox+Opal",
                 "mtgtop8": "https://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Mox+Opal"},
                 "purchase_uris": {"tcgplayer": "https://shop.tcgplayer.com/product/productsearch?id=98395&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                 "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Modern-Masters-2015/Mox-Opal?referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
                 "cardhoarder": "https://www.cardhoarder.com/cards/57258?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"}}

GOOD_RESPONSE_SETS = {
    'Judge Gift Cards 2019': {
        'usd': None,
        'usd_foil': 123.27,
    },
    'Kaladesh Inventions': {
        'usd': None,
        'usd_foil': 302.34,
    },
    'Modern Masters 2015': {
        'usd': 97.98,
        'usd_foil': 118.72,
    },
    'Scars of Mirrodin': {
        'usd': 96.37,
        'usd_foil': 196.98,
    }
}

GOOD_PAYLOAD = {'name': 'Mox Opal',
                'expansion': 'Scars of Mirrodin',
                'condition': 'NM',
                'foil': False,
                'quantity': 4}


BAD_RESPONSE = {
    "non_field_errors": [
        "There is no such card Mx Pl in Scars of Mirrodin set"
    ]
}

NULL_PRICE_RESPONSE = {
    'Judge Gift Cards 2019': {
        'usd': None,
        'usd_foil': None,
    },
    'Kaladesh Inventions': {
        'usd': None,
        'usd_foil': None,
    },
    'Modern Masters 2015': {
        'usd': None,
        'usd_foil': None,
    },
    'Scars of Mirrodin': {
        'usd': None,
        'usd_foil': None,
    }
}
