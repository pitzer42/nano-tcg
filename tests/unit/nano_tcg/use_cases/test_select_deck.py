from unittest.mock import AsyncMock

import pytest

from gameplay.nano_magic.use_cases.messages import END_DECK
from gameplay.nano_magic.use_cases.select_deck import select_deck


@pytest.mark.asyncio
async def test_request_deck_single_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list + END_DECK + '\n'
    channel = AsyncMock()
    channel.receive.return_value = response
    _cards = await select_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)


@pytest.mark.asyncio
async def test_request_deck_iterative_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list.split('\n')
    response.append(END_DECK + '\n')
    channel = AsyncMock()
    channel.receive.side_effect = response
    _cards = await select_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)
