from unittest.mock import AsyncMock

import pytest

from gameplay.nano_magic.use_cases.select_match import select_match


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
