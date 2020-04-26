import pytest
import asyncio

from functools import partial
from multiprocessing import Process

import server

from bot import TelnetBot, READ_FLAG


@pytest.fixture(scope='session')
async def running_server():
    host = '127.0.0.1'
    port = 8888
    delay = 1

    start_test_server = partial(
        server.main,
        port
    )

    server_process = Process(
        target=start_test_server
    )
    server_process.start()

    await asyncio.sleep(delay)
    yield host, port

    server_process.kill()


@pytest.fixture
def bot_factory(running_server):
    return partial(TelnetBot, *running_server)


@pytest.mark.asyncio
async def test_invalid_user_name(bot_factory):

    async with bot_factory() as client_1:
        client_1_log = await client_1.send('a')

    async with bot_factory() as client_2:
        client_2_log = await client_2.send(
            'a',
            READ_FLAG,
            'a',
            READ_FLAG,
            'b'
        )

    assert len(client_1_log) == 0
    assert len(client_2_log) == 2










