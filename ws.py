from aiohttp import web

from channels.web_socket import WebSocketChannel
from nano_magic import play
from nano_magic.adapters.client_channel import ClientChannel


async def ws_server(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await play(
        ClientChannel(
            WebSocketChannel(ws)
        )
    )
    print('websocket connection closed')


if __name__ == '__main__':
    app = web.Application()

    app.add_routes([
        web.get('/ws', ws_server)
    ])

    web.run_app(app, port=80)
