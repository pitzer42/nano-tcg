import pytest
import asyncio

from functools import partial
from multiprocessing import Process

import server
import protocol

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
@pytest.mark.skip
async def test_invalid_user_name(bot_factory):

    async with bot_factory() as client_1:
        client_1_log = await client_1.send(
            READ_FLAG,
            'a'
        )

    async with bot_factory() as client_2:
        client_2_log = await client_2.send(
            READ_FLAG,
            'a',
            READ_FLAG,
            'a',
            READ_FLAG,
            'b'
        )

    request_name_message = protocol.wrap_message(protocol.REQUEST_NAME)
    assert client_1_log == [request_name_message] * 1
    assert client_2_log == [request_name_message] * 3


@pytest.mark.asyncio
async def test_ping_pong(bot_factory):

    async with bot_factory() as a:
        async with bot_factory() as b:
            m = await a.send(
                READ_FLAG,
                'a'
            )
            print('a<'+str(m))
            m = await b.send(
                READ_FLAG,
                'b'
            )
            print('b<'+str(m))
            m = await a.send(
                READ_FLAG,
                'foo'
            )
            print('a<'+str(m))
            m = await b.send(
                READ_FLAG,
                READ_FLAG,
                'bar'
            )
            print('b<'+str(m))