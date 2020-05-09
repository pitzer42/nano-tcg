from unittest.mock import AsyncMock

import pytest

from gameplay.nano_magic import protocol
from gameplay.nano_magic.match import request_match, draw, prompt_mulligan, draw_initial_hand


@pytest.mark.asyncio
async def test_request_match_new():
    id = test_request_match_new.__name__
    password = test_request_match_new.__name__ + '123'
    channel = AsyncMock()
    channel.receive.side_effect = [id, password]

    _id, _password = await request_match(
        channel,
        lambda _: True,
        lambda _: True)

    assert _id == id
    assert _password == password


@pytest.mark.asyncio
async def test_request_match_n_wrong_passwords():
    n_mistakes = 3
    id = test_request_match_n_wrong_passwords.__name__
    wrong_password = test_request_match_n_wrong_passwords.__name__ + '123'
    correct_password = test_request_match_n_wrong_passwords.__name__ + '456'

    channel = AsyncMock()
    channel.receive.side_effect = ([id, wrong_password] * n_mistakes) + [id, correct_password]

    _id, _password = await request_match(
        channel,
        lambda _: False,
        lambda _: correct_password)

    assert _id == id
    assert _password == correct_password


@pytest.mark.asyncio
async def test_draw_initial_hand():
    hand_size = 7
    deck = list(range(60))
    original_deck = list(deck)
    channel = AsyncMock()
    hand = await draw_initial_hand(channel, deck, hand_size)
    assert len(hand) == hand_size
    assert len(deck) == len(original_deck) - hand_size


@pytest.mark.asyncio
async def test_hand_size_zero_is_stop_condition():
    hand_size = 0
    deck = [1, 2, 3]
    original_deck = list(deck)
    channel = AsyncMock()
    await draw_initial_hand(channel, deck, hand_size)
    channel.send.assert_not_called()
    channel.receive.assert_not_called()
    assert deck == original_deck


@pytest.mark.asyncio
async def test_deck_was_shuffled_before_draw_initial_hand():
    """
    assert that the deck order changed more than a epsilon ratio
    """
    episolon = 0.5
    epoches = 3
    hand_size = 7
    deck_size = 60
    channel = AsyncMock()
    deck = list(range(60))
    original_deck = list(deck)
    positives = 0

    for i in range(epoches):
        hand = await draw_initial_hand(
            channel,
            deck,
            hand_size)
        if deck != original_deck[:-hand_size]:
            positives += 1

    assert (positives / epoches) > episolon


@pytest.mark.asyncio
async def test_prompt_mulligan_accept():
    channel = AsyncMock()
    hand = [1, 2, 3]
    message = protocol.prompt_mulligan(hand)
    channel.receive.return_value = protocol.POSITIVES[0]
    accepted_mulligan = await prompt_mulligan(channel, hand)
    assert accepted_mulligan
    channel.send.was_called_with(message)


@pytest.mark.asyncio
async def test_prompt_mulligan_reject():
    channel = AsyncMock()
    hand = [1, 2, 3]
    message = protocol.prompt_mulligan(hand)
    """
    the sum of all elements in a set does not belong to the set.
    sum(range(10)) not in range(10)
    """
    channel.receive.return_value = ''.join(protocol.POSITIVES)
    accepted_mulligan = await prompt_mulligan(channel, hand)
    assert not accepted_mulligan
    channel.send.was_called_with(message)


def test_draw():
    n = 1
    deck = [1, 2, 3]
    hand = []
    draw(n, deck, hand)
    assert deck == [1, 2]
    assert hand == [3]
