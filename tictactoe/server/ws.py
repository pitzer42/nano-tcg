import os

from aiohttp import web

from gloop.channels.bases.redis import RedisChannel
from gloop.channels.bases.web_socket import WebSocketChannel
from tictactoe.adapters.client_channel import TicTacToeClientChannel
from tictactoe.adapters.match_channel import TicTacToeMatchClient
from tictactoe.storage.memory import TicTacToePlayerMemoryRepository, TicTacToeMatchMemoryRepository
from tictactoe.use_cases.game_loop import TicTacToeGameLoop


async def create_redis_channel(topic):
    return RedisChannel(
        topic,
        'redis://localhost:6379'
    )


async def create_match_client(match):
    inner_channel = await create_redis_channel(match.id)
    return TicTacToeMatchClient(inner_channel)


async def ws_server(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client_channel = TicTacToeClientChannel(
        WebSocketChannel(ws)
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


if __name__ == '__main__':
    port = os.environ.get('PORT', 8080)
    statics_path = '../tictactoe/ui'
    page = statics_path + '/app.html'

    app = web.Application()

    app.add_routes([
        web.get('/ws', ws_server),
        web.get('/', lambda request: web.FileResponse(page)),
        web.static('/static', statics_path)
    ])

    web.run_app(
        app,
        port=port
    )
