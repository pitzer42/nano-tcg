from unittest.mock import AsyncMock

import pytest

from nano_magic.entities.match import Match
from nano_magic.use_cases.select_match import select_match


@pytest.mark.asyncio
async def test_request_match_new():
    expected_id = 'match0'
    expected_password = 'password0'
    matches = dict()
    client = AsyncMock()
    client.request_match_id.return_value = expected_id
    client.request_match_password.return_value = expected_password
    match = await select_match(client, matches)
    assert match.id == expected_id
    assert match.check_password(expected_password)


@pytest.mark.asyncio
async def test_request_match_n_wrong_passwords():
    n_mistakes = 3
    expected_id = 'match0'
    expected_password = 'password0'
    wrong_password = 'password1'
    matches = dict()
    matches[expected_id] = Match(
        expected_id,
        expected_password
    )
    client = AsyncMock()
    client.request_match_id.return_value = expected_id
    provided_passwords = [wrong_password] * n_mistakes
    provided_passwords.append(expected_password)
    client.request_match_password.side_effect = provided_passwords
    match = await select_match(client, matches)
    assert client.request_match_password.await_count == n_mistakes + 1
    assert match.id == expected_id
    assert match.check_password(expected_password)
