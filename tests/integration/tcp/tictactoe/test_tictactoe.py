import json

import pytest

from tests.integration.tcp.bot import READ_FLAG


@pytest.mark.asyncio
async def test_tictactoe(tcp_bot_factory):
    async with tcp_bot_factory() as player_a:
        async with tcp_bot_factory() as player_b:
            log_a = await player_a.send(
                READ_FLAG,
                '{"player_id": "foo"}',
                READ_FLAG,
                '{"match_id": "m1", "password": "p1"}'
            )

            log_b = await player_b.send(
                READ_FLAG,
                '{"player_id": "bar"}',
                READ_FLAG,
                '{"match_id": "m1", "password": "p1"}'
            )

            log_a = await player_a.send(READ_FLAG)
            log_b = await player_b.send(READ_FLAG)
            response_a = json.loads(log_a[0])
            response_b = json.loads(log_b[0])
            assert response_a['message'] == 'sync'
            assert response_b['message'] == 'sync'

            log_a = await player_b.send(READ_FLAG)
