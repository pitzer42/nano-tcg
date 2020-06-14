import asyncio
import sys
from functools import partial

from channels.aio_stream import AioStreamChannel
from channels.redis import RedisChannel
from tictactoe.adapters.client_channel import ClientChannel
from tictactoe.storage.memory import MemoryMatchRepository, MemoryPlayerRepository
from tictactoe.use_cases.game_loop import game_loop as game_loop

"""
from nano_magic import play as game_play
from nano_magic.adapters.client_channel import ClientChannel
"""


async def create_redis_channel(topic):
    return RedisChannel(
        topic,
        'redis://localhost:6379'
    )


async def accept_streams(accept, reader, writer):
    await accept(
        ClientChannel(
            AioStreamChannel(
                reader,
                writer
            )
        ),
        MemoryMatchRepository(),
        MemoryPlayerRepository(),
        create_redis_channel
    )


async def start_server(accept, host, port):
    print(f'starting {host}:{port}')
    accept = partial(accept_streams, accept)
    server = await asyncio.start_server(
        accept,
        host,
        port
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':

    _host = '127.0.0.1'
    _port = 8888
    _accept = game_loop

    if len(sys.argv) > 1:
        _port = int(sys.argv[1])

    asyncio.run(
        start_server(
            _accept,
            _host,
            _port
        )
    )
