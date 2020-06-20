from unittest.mock import AsyncMock

import pytest

from features.identify_client.feature import IdentifyClient


@pytest.mark.asyncio
async def test_identify_client_with_available_id():
    expected_id = 42

    client = AsyncMock()
    client.request_client_id.return_value = expected_id

    repo = AsyncMock()
    repo.is_client_id_available.return_value = True

    feature = IdentifyClient(
        client,
        repo
    )

    result = await feature.execute()
    assert result == expected_id


@pytest.mark.asyncio
async def test_identify_client_with_unavailable_id():
    available_id = 42
    unavailable_id = 41

    client = AsyncMock()
    client.request_client_id.side_effect = [
        unavailable_id,
        available_id
    ]

    repo = AsyncMock()
    repo.is_client_id_available.side_effect = [
        False,
        True
    ]

    feature = IdentifyClient(
        client,
        repo
    )

    result = await feature.execute()
    assert result == available_id


@pytest.mark.asyncio
async def test_repeat_identify_client_until_available_id_is_provided():
    repeat = 2
    available_id = 42
    unavailable_id = 41

    client = AsyncMock()
    client.request_client_id.side_effect = [unavailable_id] * repeat + [available_id]

    repo = AsyncMock()
    repo.is_client_id_available.side_effect = [False] * repeat + [True]

    feature = IdentifyClient(
        client,
        repo
    )

    result = await feature.execute()
    assert result == available_id
    assert client.request_client_id.await_count == repeat + 1
