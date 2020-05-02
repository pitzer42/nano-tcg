import pytest

from functools import partial

import server
import asyncio

from multiprocessing import Process

from gameplay.nano_magic import protocol

from tests.integration.tcp.bot import READ_FLAG, TcpBot


@pytest.fixture
def tcp_bot_factory(running_server):
    host, port = running_server
    return partial(TcpBot, host, port)


@pytest.fixture
async def running_server(unused_tcp_port):
    host = '127.0.0.1'
    port = unused_tcp_port
    startup_delay_secs = 1

    start_test_server = partial(server.main, port)
    server_process = Process(target=start_test_server)
    server_process.start()
    await asyncio.sleep(startup_delay_secs)

    yield host, port

    server_process.kill()
