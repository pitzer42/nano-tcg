from unittest.mock import AsyncMock

import pytest

from nano_magic.adapters import messages
from nano_magic.adapters.messages import END_DECK
from nano_magic.use_cases.select_deck import select_deck


@pytest.mark.asyncio
@pytest.mark.skip
async def test_request_deck_single_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list + END_DECK + '\n'
    channel = AsyncMock()
    channel.receive.return_value = response
    _cards = await select_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_request_deck_iterative_response_quantity_and_blank_lines(deck_list, cards, deck_length):
    response = deck_list.split('\n')
    response.append(END_DECK + '\n')
    channel = AsyncMock()
    channel.receive.side_effect = response
    _cards = await select_deck(channel)
    assert END_DECK not in cards
    assert _cards == cards
    channel.send_was_called_with(deck_length)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_prompt_mulligan_accept():
    player = AsyncMock()
    player.hand = [1, 2, 3]
    message = messages.prompt_mulligan(player.hand)
    player.receive.return_value = messages.POSITIVES[0]
    # accepted_mulligan = await _prompt_mulligan(player, player.hand)
    # assert accepted_mulligan
    player.send.was_called_with(message)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_prompt_mulligan_reject():
    player = AsyncMock()
    player.hand = [1, 2, 3]
    message = messages.prompt_mulligan(player.hand)
    """
    the sum of all elements in a set does not belong to the set.
    sum(range(10)) not in range(10)
    """
    player.receive.return_value = ''.join(messages.POSITIVES)
    # accepted_mulligan = await _prompt_mulligan(player, player.hand)
    # assert not accepted_mulligan
    player.send.was_called_with(message)
