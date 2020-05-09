import pytest
from unittest.mock import AsyncMock


from gameplay.nano_magic.login import request_name


@pytest.mark.asyncio
async def test_request_name():
    expected_name = test_request_name.__name__
    channel = AsyncMock()
    channel.receive.return_value = expected_name
    name = await request_name(channel, lambda _: True)
    assert name == expected_name


@pytest.mark.asyncio
async def test_request_name_retry():
    n_retries = 10
    invalid_name = 'invalid_' + test_request_name.__name__
    names = [invalid_name] * n_retries

    expected_name = test_request_name.__name__
    names.append(expected_name)

    channel = AsyncMock()
    channel.receive.side_effect = names

    name = await request_name(
        channel,
        lambda n: n != invalid_name
    )

    assert name == expected_name


