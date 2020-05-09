from unittest.mock import AsyncMock

import pytest

from gameplay.nano_magic.deck import request_deck, parse_deck_str
from gameplay.nano_magic.protocol import END_DECK


@pytest.fixture
def cards() -> list:
    return ['grim lavamancer', 'grim lavamancer', 'restoration angel', 'restoration angel', 'vendilion clique',
            'vendilion clique', 'snapcaster mage', 'snapcaster mage', 'snapcaster mage', 'snapcaster mage',
            'spell queller', 'spell queller', 'spell queller', 'spell queller', 'teferi, time raveler',
            'teferi, time raveler', 'teferi, time raveler', "dovin's veto", "dovin's veto", 'lightning helix',
            'lightning helix', 'lightning helix', 'lightning bolt', 'lightning bolt', 'lightning bolt',
            'lightning bolt', 'opt', 'opt', 'opt', 'opt', 'path to exile', 'path to exile', 'path to exile',
            'path to exile', 'spreading seas', 'spreading seas', 'mountain', 'plains', 'island', 'island', 'arid mesa',
            'glacial fortress', 'sacred foundry', 'spirebluff canal', 'sulfur falls', 'celestial colonnade',
            'celestial colonnade', 'field of ruin', 'field of ruin', 'hallowed fountain', 'hallowed fountain',
            'steam vents', 'steam vents', 'scalding tarn', 'scalding tarn', 'scalding tarn', 'flooded strand',
            'flooded strand', 'flooded strand', 'flooded strand', 'abrade', 'ashiok, dream render',
            'ashiok, dream render', 'celestial purge', 'detention sphere', 'detention sphere', 'disdainful stroke',
            'force of negation', 'force of negation', 'magma spray', 'stony silence', 'stony silence',
            'surgical extraction', 'surgical extraction', 'surgical extraction']


@pytest.fixture
def deck_list() -> str:
    return """
        2 Grim Lavamancer
        2 Restoration Angel
        2 Vendilion Clique
        4 Snapcaster Mage
        4 Spell Queller
        3 Teferi, Time Raveler
        2 Dovin's Veto
        3 Lightning Helix
        4 Lightning Bolt
        4 Opt
        4 Path to Exile
        2 Spreading Seas
        1 Mountain
        1 Plains
        2 Island
        1 Arid Mesa
        1 Glacial Fortress
        1 Sacred Foundry
        1 Spirebluff Canal
        1 Sulfur Falls
        2 Celestial Colonnade
        2 Field of Ruin
        2 Hallowed Fountain
        2 Steam Vents
        3 Scalding Tarn
        4 Flooded Strand

        1 Abrade
        2 Ashiok, Dream Render
        1 Celestial Purge
        2 Detention Sphere
        1 Disdainful Stroke
        2 Force of Negation
        1 Magma Spray
        2 Stony Silence
        3 Surgical Extraction
        """


@pytest.fixture
def deck_length(cards) -> str:
    return len(cards)


def test_parse_deck(deck_list, cards, deck_length):
    _cards = parse_deck_str(deck_list)
    _deck_length = len(_cards)
    assert _cards == cards
    assert _deck_length == deck_length


@pytest.mark.asyncio
async def test_request_deck_single_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list + END_DECK + '\n'
    channel = AsyncMock()
    channel.receive.return_value = response
    _cards = await request_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)


@pytest.mark.asyncio
async def test_request_deck_iterative_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list.split('\n')
    response.append(END_DECK + '\n')
    channel = AsyncMock()
    channel.receive.side_effect = response
    _cards = await request_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)
