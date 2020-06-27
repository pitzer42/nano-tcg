import asyncio
import sys

from channels.bases.aio_stream import AioStreamChannel
from channels.bases.redis import RedisChannel
from tictactoe.adapters.client_channel import TicTacToeClientChannel
from tictactoe.adapters.match_channel import TicTacToeMatchClient
from tictactoe.game_loop import TicTacToeGameLoop
from tictactoe.storage.memory import TicTacToeMatchMemoryRepository, TicTacToePlayerMemoryRepository


async def create_redis_channel(topic):
    return RedisChannel(
        topic,
        'redis://localhost:6379'
    )


async def create_match_client(match):
    inner_channel = await create_redis_channel(match.id)
    return TicTacToeMatchClient(inner_channel)


async def start_game_loop(reader, writer):
    client_channel = TicTacToeClientChannel(
        AioStreamChannel(
            reader,
            writer
        )
    )
    players = TicTacToePlayerMemoryRepository()
    matches = TicTacToeMatchMemoryRepository()
    game_loop = TicTacToeGameLoop(
        client_channel,
        players,
        matches,
        create_match_client
    )

    await game_loop.execute()


async def start_server(host, port):
    print(f'starting {host}:{port}')

    server = await asyncio.start_server(
        start_game_loop,
        host,
        port
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':

    _host = '127.0.0.1'
    _port = 8888

    if len(sys.argv) > 1:
        _port = int(sys.argv[1])

    asyncio.run(
        start_server(
            _host,
            _port
        )
    )
