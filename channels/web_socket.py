from channels import Channel
from aiohttp.web import WebSocketResponse

class WebSocketChannel(Channel):

    def __init__(self, ws: WebSocketResponse):
        super(WebSocketChannel, self).__init__()
        self._ws = ws

    async def connect(self):
        pass

    async def close(self):
        await self._ws.close()

    async def send(self, packet: bytes):
        await self._ws.send_bytes(packet)

    async def receive(self) -> bytes:
        return await self._ws.receive_bytes()
