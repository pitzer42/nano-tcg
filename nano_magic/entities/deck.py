import random

from typing import List, AnyStr

ENTRY_SEPARATOR = '\n'
WORD_SEPARATOR = ' '
MULTIPLIER_SIGN = 'x'


def shuffle(deck: List[AnyStr]):
    if len(deck) > 0:
        random.seed(id(deck) + id(deck[0]))
        random.shuffle(deck)


def deck_parser(deck_str: str):
    cards = list()
    deck_str = deck_str.split(ENTRY_SEPARATOR)
    for deck_entry in deck_str:
        deck_entry = deck_entry.strip().lower()
        if not deck_entry:
            continue
        try:
            first_space_index = deck_entry.index(WORD_SEPARATOR)
            quantity_str = deck_entry[:first_space_index]
            quantity_str.replace(MULTIPLIER_SIGN, str())
            quantity_str = quantity_str.strip()
            quantity = int(quantity_str)
            card = deck_entry[first_space_index + 1:]
            card = card.strip()
        except:
            quantity = 1
            card = deck_entry.strip()

        cards += [card] * quantity

    return cards
