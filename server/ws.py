import os
from functools import partial

from aiohttp import web

from channels.bases.web_socket import WebSocketChannel
from nano_magic import play as game_play
from nano_magic.adapters.client_channel import ClientChannel


async def ws_server(accept, request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await accept(
        ClientChannel(
            WebSocketChannel(ws)
        )
    )


if __name__ == '__main__':
    port = os.environ.get('PORT', 8080)

    app = web.Application()
    server = partial(ws_server, game_play)

    app.add_routes([
        web.get('/ws', server),
        web.get('/', lambda request: web.FileResponse('../ui/front.html')),
        web.static('/static', '../ui')
    ])

    web.run_app(
        app,
        port=port
    )
