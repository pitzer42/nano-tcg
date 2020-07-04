from unittest.mock import Mock, AsyncMock

import pytest

from gloop.features import JoinMatch
from gloop.features import MatchAlreadyReadyException


@pytest.mark.asyncio
async def test_join_match():
    expected_match = AsyncMock()
    expected_match.is_ready.return_value = True

    client = AsyncMock()

    repo = AsyncMock()
    repo.join_and_get_if_still_waiting.return_value = expected_match

    feature = JoinMatch(
        client,
        repo
    )

    result = await feature.execute(
        Mock(),
        Mock()
    )
    repo.join_and_get_if_still_waiting.assert_awaited()


@pytest.mark.asyncio
async def test_join_match_already_ready():
    expected_match = AsyncMock()
    expected_match.is_ready.return_value = True

    client = AsyncMock()

    repo = AsyncMock()
    repo.join_and_get_if_still_waiting.side_effect = MatchAlreadyReadyException()

    feature = JoinMatch(
        client,
        repo
    )

    with pytest.raises(MatchAlreadyReadyException):
        result = await feature.execute(
            Mock(),
            Mock()
        )
