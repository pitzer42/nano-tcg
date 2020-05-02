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

    async def send(self, message: str):
        await self._ws.send_str(message)

    async def receive(self) -> str:
        return await self._ws.receive_str()
