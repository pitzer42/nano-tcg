from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest


@pytest.mark.asyncio
async def test_create_match():
    created_match = 'created_match'

    client = AsyncMock()
    client.request_match_id_and_password.return_value = 0, 0
    client.alert_wrong_match_password.return_value = AsyncMock()
    client.alert_match_creation_exception.return_value = AsyncMock()

    repo = AsyncMock()
    repo.get_by_id.return_value = None

    async def match_factory(a, b):
        return created_match

    feature = SelectOrCreateMatch(
        client,
        repo,
        match_factory
    )

    result = await feature.execute()
    assert result == created_match


@pytest.mark.asyncio
async def test_select_match():
    select_match = AsyncMock()
    select_match.check_password.return_value = True

    client = AsyncMock()
    client.request_match_id_and_password.return_value = 0, 0
    client.alert_wrong_match_password.return_value = AsyncMock()
    client.alert_match_creation_exception.return_value = AsyncMock()

    repo = AsyncMock()
    repo.get_waiting_matches.return_value = []
    repo.get_by_id.return_value = select_match

    feature = SelectOrCreateMatch(
        client,
        repo,
        AsyncMock()
    )

    result = await feature.execute()
    assert result == select_match


@pytest.mark.asyncio
async def test_select_match_and_n_wrong_password():
    retries = 10
    select_match = Mock()
    select_match.check_password.side_effect = [False] * retries + [True]

    client = AsyncMock()
    client.request_match_id_and_password.side_effect = [(0, 0)] * retries + [(0, 1)]
    client.alert_wrong_match_password.return_value = AsyncMock()
    client.alert_match_creation_exception.return_value = AsyncMock()

    repo = AsyncMock()
    repo.get_waiting_matches.return_value = []
    repo.get_by_id.return_value = select_match

    feature = SelectOrCreateMatch(
        client,
        repo,
        AsyncMock()
    )

    result = await feature.execute()
    assert result == select_match
    assert repo.get_by_id.await_count == retries + 1
    client.alert_wrong_match_password.await_count == retries
