from unittest.mock import AsyncMock

import pytest

from nano_magic.use_cases.login import request_available_user_id, login


@pytest.mark.asyncio
async def test_request_available_user_id():
    players = dict()
    expected_id = 'player0'
    client = AsyncMock()
    client.request_player_id.return_value = expected_id
    provided_id = await request_available_user_id(client, players)
    client.request_player_id.assert_awaited()
    assert provided_id == expected_id


@pytest.mark.asyncio
async def test_request_available_user_id_retry():
    n_retries = 10
    available_id = 'player0'
    unavailable_id = 'player1'
    provided_ids = [unavailable_id] * n_retries
    provided_ids.append(available_id)
    players = dict()
    players[unavailable_id] = None

    client = AsyncMock()
    client.request_player_id.side_effect = provided_ids

    provided_id = await request_available_user_id(
        client,
        players
    )

    assert provided_id == available_id


@pytest.mark.asyncio
async def test_login():
    expected_id = 'player0'
    client = AsyncMock()
    client.request_player_id.return_value = expected_id
    players = dict()
    player = await login(client, players)
    assert player.id == expected_id
