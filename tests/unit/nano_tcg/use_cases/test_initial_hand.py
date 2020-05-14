from unittest.mock import AsyncMock

import pytest

from gameplay.nano_magic.use_cases import messages
from gameplay.nano_magic.use_cases.initial_hand import _prompt_mulligan, draw_initial_hand


@pytest.mark.asyncio
async def test_draw_initial_hand():
    player = AsyncMock()
    player.deck = list(range(60))
    original_deck = list(player.deck)
    hand_size = 7
    hand = await draw_initial_hand(player, hand_size)
    assert len(hand) == hand_size
    assert len(player.deck) == len(original_deck) - hand_size


@pytest.mark.asyncio
async def test_hand_size_zero_is_stop_condition():
    player = AsyncMock()
    player.deck = [1, 2, 3]
    original_deck = list(player.deck)
    hand_size = 0
    await draw_initial_hand(player, hand_size)
    player.send.assert_not_called()
    player.receive.assert_not_called()
    assert player.deck == original_deck


@pytest.mark.asyncio
async def test_deck_was_shuffled_before_draw_initial_hand():
    """
    assert that the deck order changed more than a epsilon ratio
    """
    episolon = 0.5
    epoches = 3
    hand_size = 7
    deck_size = 60
    player = AsyncMock()
    player.deck = list(range(deck_size))
    original_deck = list(player.deck)
    positives = 0

    for i in range(epoches):
        hand = await draw_initial_hand(player, hand_size)
        if player.deck != original_deck[:-hand_size]:
            positives += 1

    assert (positives / epoches) > episolon


@pytest.mark.asyncio
async def test_prompt_mulligan_accept():
    player = AsyncMock()
    player.hand = [1, 2, 3]
    message = messages.prompt_mulligan(player.hand)
    player.receive.return_value = messages.POSITIVES[0]
    accepted_mulligan = await _prompt_mulligan(player, player.hand)
    assert accepted_mulligan
    player.send.was_called_with(message)


@pytest.mark.asyncio
async def test_prompt_mulligan_reject():
    player = AsyncMock()
    player.hand = [1, 2, 3]
    message = messages.prompt_mulligan(player.hand)
    """
    the sum of all elements in a set does not belong to the set.
    sum(range(10)) not in range(10)
    """
    player.receive.return_value = ''.join(messages.POSITIVES)
    accepted_mulligan = await _prompt_mulligan(player, player.hand)
    assert not accepted_mulligan
    player.send.was_called_with(message)