from aiohttp import web
from channels.web_socket import WebSocketChannel
from modes.nano_magic import accept2

async def ws_server(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    channel = WebSocketChannel(ws)
    await accept2(ws)
    print('websocket connection closed')

if __name__ == '__main__':

    app = web.Application()

    app.add_routes([
        web.get('/', ws_server)
    ])

    web.run_app(app)