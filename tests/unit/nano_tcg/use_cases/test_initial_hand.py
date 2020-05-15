from unittest.mock import AsyncMock

import pytest

from nano_magic.use_cases.initial_hand import draw_initial_hand, INITIAL_HAND_SIZE


@pytest.mark.asyncio
async def test_draw_initial_hand():
    client = AsyncMock()
    client.prompt_mulligan.return_value = False
    deck = list(range(60))
    original_deck = list(deck)
    hand = await draw_initial_hand(client, deck)
    client.prompt_mulligan.assert_awaited_with(hand)
    assert len(hand) == INITIAL_HAND_SIZE
    assert len(deck) == len(original_deck) - INITIAL_HAND_SIZE


@pytest.mark.asyncio
async def test_mulligan_more_than_initial_hand_size_times():
    client = AsyncMock()
    client.prompt_mulligan.side_effect = [True] * INITIAL_HAND_SIZE
    deck = list(range(60))
    original_deck = list(deck)
    hand = await draw_initial_hand(client, deck)
    assert len(hand) == 0
    assert client.prompt_mulligan.await_count == INITIAL_HAND_SIZE
    assert len(deck) == len(original_deck)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_hand_size_zero_is_stop_condition():
    client = AsyncMock()
    deck = [1, 2, 3]
    original_deck = list(deck)
    hand_size = 0
    await draw_initial_hand(client, deck, hand_size)
    client.send.assert_not_called()
    client.receive.assert_not_called()
    assert client.deck == original_deck
