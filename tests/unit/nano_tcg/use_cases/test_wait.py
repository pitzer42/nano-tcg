from unittest.mock import AsyncMock, Mock

import pytest

from nano_magic.use_cases.waiting import join


@pytest.mark.asyncio
async def test_join():
    player = Mock()
    match = AsyncMock()
    client = AsyncMock()
    join(client, player, match)
    assert client.send_wait.was_awaited()
    assert match.join.was_called_with(player)
    assert match.to_be_ready.was_awaited()
