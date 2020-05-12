from gameplay.nano_magic.entities.deck import deck_parser


def test_parse_deck(deck_list, cards, deck_length):
    _cards = deck_parser(deck_list)
    _deck_length = len(_cards)
    assert _cards == cards
    assert _deck_length == deck_length
