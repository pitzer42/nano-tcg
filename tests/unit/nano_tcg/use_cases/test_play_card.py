from unittest.mock import AsyncMock

import pytest

from nano_magic.use_cases.main_phase import play_card


@pytest.mark.asyncio
async def test_play_one_card_from_hand():
    hand_size = 7
    client = AsyncMock()
    client.request_card_in_hand.side_effect = [0, -1]
    hand = list(range(hand_size))
    board = list()
    await play_card(
        client,
        hand,
        board
    )
    assert 0 in board
    assert len(board) == 1
    assert 0 not in hand
    assert len(hand) == hand_size - 1


@pytest.mark.asyncio
async def test_do_not_play_card_from_hand():
    hand_size = 7
    client = AsyncMock()
    client.request_card_in_hand.side_effect = [-1]
    hand = list(range(hand_size))
    board = list()
    await play_card(
        client,
        hand,
        board
    )
    assert len(board) == 0
    assert len(hand) == hand_size
