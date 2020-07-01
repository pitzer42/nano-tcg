from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from features.onboard.feature import Onboard


@pytest.fixture
def onboard():
    def player_factory(player_id):
        mock = Mock()
        mock.id = player_id
        return mock

    return Onboard(
        AsyncMock(),
        player_factory,
        AsyncMock(),
        AsyncMock,
        AsyncMock(),
        AsyncMock
    )


@pytest.mark.asyncio
async def test_identify_client_with_available_id(onboard):
    expected_id = 42

    client = AsyncMock()
    client.request_client_id.return_value = expected_id

    onboard.player_repo.is_client_id_available.return_value = True

    player = await onboard.login()
    assert player.id == expected_id


@pytest.mark.asyncio
async def test_identify_client_with_unavailable_id(onboard):
    available_id = 42
    unavailable_id = 41

    client = AsyncMock()
    client.request_client_id.side_effect = [
        unavailable_id,
        available_id
    ]

    onboard.player_repo.is_client_id_available.side_effect = [
        False,
        True
    ]

    player = await onboard.login()
    assert player.id == available_id


@pytest.mark.asyncio
async def test_repeat_identify_client_until_available_id_is_provided(onboard):
    repeat = 10
    available_id = 42
    unavailable_id = 41

    client = AsyncMock()
    client.request_client_id.side_effect = [unavailable_id] * repeat + [available_id]

    onboard.player_repo.is_client_id_available.side_effect = [False] * repeat + [True]

    player = await onboard.login()
    assert player.id == available_id
    assert client.request_client_id.await_count == repeat + 1
