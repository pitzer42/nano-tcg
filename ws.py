from aiohttp import web
from modes.nano_magic import accept
from channels.web_socket import WebSocketChannel


async def ws_server(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    channel = WebSocketChannel(ws)
    await accept(channel)
    print('websocket connection closed')


if __name__ == '__main__':
    app = web.Application()

    app.add_routes([
        web.get('/ws', ws_server)
    ])

    web.run_app(app)