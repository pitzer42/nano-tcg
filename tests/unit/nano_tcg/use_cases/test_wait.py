from unittest.mock import AsyncMock, Mock

import pytest

from nano_magic.use_cases.waiting import join


@pytest.mark.asyncio
async def test_join():
    player = Mock()
    match = AsyncMock()
    client = AsyncMock()
    await join(client, player, match)
    client.send_wait.assert_awaited()
    match.to_be_ready.assert_awaited()
    match.join.assert_called_with(player)
