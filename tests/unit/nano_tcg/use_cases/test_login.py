from unittest.mock import AsyncMock

import pytest

from nano_magic.use_cases import request_player_id


@pytest.mark.asyncio
async def test_request_player_id():
    expected_name = test_request_player_id.__name__
    channel = AsyncMock()
    channel.receive.return_value = expected_name
    name = await request_player_id(channel, lambda _: True)
    assert name == expected_name


@pytest.mark.asyncio
async def test_request_player_id_retry():
    n_retries = 10
    invalid_name = 'invalid_' + test_request_player_id.__name__
    names = [invalid_name] * n_retries

    expected_name = test_request_player_id.__name__
    names.append(expected_name)

    channel = AsyncMock()
    channel.receive.side_effect = names

    name = await request_player_id(
        channel,
        lambda n: n != invalid_name
    )

    assert name == expected_name
