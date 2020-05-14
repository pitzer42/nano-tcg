from nano_magic.entities.deck import deck_parser, shuffle


def test_parse_deck(deck_list, cards, deck_length):
    _cards = deck_parser(deck_list)
    _deck_length = len(_cards)
    assert _cards == cards
    assert _deck_length == deck_length


def test_shuffle(cards):
    """
    assert that the deck order changed more than a epsilon ratio
    """
    epsilon = 0.999
    epochs = 30
    original = list(cards)
    positives = 0

    for i in range(epochs):
        subject = list(cards)
        shuffle(subject)
        if subject != original:
            positives += 1

    assert (positives / epochs) > epsilon
