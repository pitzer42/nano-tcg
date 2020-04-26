import pytest
import asyncio

from functools import partial
from multiprocessing import Process

import server

from bot import lang
from bot import ClientBot


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
def execute_client(running_server):

    async def execute(*instructions):
        bot = ClientBot()
        bot.set_instructions(instructions)
        await bot.connect(
            *running_server
        )
        logs = await bot.run()
        await bot.close()
        return logs

    return execute


@pytest.mark.asyncio
async def test_invalid_user_name(execute_client):

    client_log_1 = await execute_client(
        'a'
    )

    client_log_2 = await execute_client(
        'a',
        lang.read_command,
        'a',
        lang.read_command,
        'b'
    )

    assert len(client_log_1) == 0
    assert len(client_log_2) == 2










