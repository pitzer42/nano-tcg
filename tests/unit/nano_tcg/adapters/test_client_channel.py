from unittest.mock import AsyncMock

import pytest

from nano_magic.adapters.client_channel import ClientChannel
from nano_magic.adapters.messages import END_DECK
from nano_magic.adapters.messages import POSITIVES


@pytest.fixture
def cards():
    return [str(i) for i in range(7)]


@pytest.mark.asyncio
async def test_request_player_id():
    expected_id = '0'
    channel = AsyncMock()
    channel.receive.return_value = expected_id
    client = ClientChannel(channel)
    player_id = await client.request_player_id()
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(player_id) is str
    assert expected_id == player_id


@pytest.mark.asyncio
async def test_request_deck(cards):
    channel = AsyncMock()
    cards.append(END_DECK)
    channel.receive.side_effect = cards
    client = ClientChannel(channel)
    deck_entries = [i async for i in client.request_deck()]
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert len(deck_entries) == len(cards) - 1
    assert type(deck_entries) is list
    assert type(deck_entries[0]) is str
    assert deck_entries == cards[:-1]


@pytest.mark.asyncio
async def test_request_match_id():
    channel = AsyncMock()
    expected_id = '0'
    channel.receive.return_value = expected_id
    client = ClientChannel(channel)
    match_id = await client.request_match_id()
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(match_id) is str
    assert expected_id == match_id


@pytest.mark.asyncio
async def test_request_match_password():
    channel = AsyncMock()
    expected_password = '0'
    channel.receive.return_value = expected_password
    client = ClientChannel(channel)
    password = await client.request_match_password()
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(password) is str
    assert expected_password == password


@pytest.mark.asyncio
async def test_prompt_mulligan_positive(cards):
    channel = AsyncMock()
    expected_answer = POSITIVES[0]
    channel.receive.return_value = expected_answer
    client = ClientChannel(channel)
    mulligan = await client.prompt_mulligan(cards)
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(mulligan) is bool
    assert mulligan


@pytest.mark.asyncio
async def test_prompt_mulligan_negative(cards):
    channel = AsyncMock()
    # the sum of all elements in a set does not belong to the set.
    # sum(range(10)) not in range(10)
    expected_answer = ''.join(POSITIVES)
    channel.receive.return_value = expected_answer
    client = ClientChannel(channel)
    mulligan = await client.prompt_mulligan(cards)
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(mulligan) is bool
    assert not mulligan


@pytest.mark.asyncio
async def test_request_card_in_hand(cards):
    channel = AsyncMock()
    client = ClientChannel(channel)
    expected_index = 0
    channel.receive.return_value = str(expected_index)
    index = await client.request_card_in_hand(cards)
    channel.send.assert_awaited()
    channel.receive.assert_awaited()
    assert type(index) is int
    assert index == expected_index


@pytest.mark.asyncio
async def test_set_hand(cards):
    channel = AsyncMock()
    client = ClientChannel(channel)
    await client.set_hand(cards)
    channel.send.assert_awaited()


@pytest.mark.asyncio
async def test_send_wait():
    channel = AsyncMock()
    client = ClientChannel(channel)
    await client.send_wait()
    channel.send.assert_awaited()


@pytest.mark.asyncio
async def test_set_board(cards):
    channel = AsyncMock()
    client = ClientChannel(channel)
    await client.set_board(cards)
    channel.send.assert_awaited()
