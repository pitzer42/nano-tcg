import asyncio
from functools import partial
from multiprocessing import Process

import pytest

from server.tcp import start_server
from tests.integration.tcp.bot import TcpBot


@pytest.fixture
def game_play():
    import nano_magic
    return nano_magic.play


@pytest.fixture
def tcp_bot_factory(running_server):
    host, port = running_server
    return partial(TcpBot, host, port)


@pytest.fixture
async def running_server(unused_tcp_port, game_play):
    host = '127.0.0.1'
    port = unused_tcp_port
    startup_delay_secs = 1

    # yield host, 8888
    # return

    def start_server_async():
        asyncio.run(
            start_server(
                game_play,
                host,
                port
            )
        )

    server_process = Process(target=start_server_async)
    server_process.start()
    await asyncio.sleep(startup_delay_secs)

    yield host, port

    server_process.kill()
