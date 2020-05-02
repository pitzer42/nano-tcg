import asyncio

from channels.aio_stream import AioStreamChannel


class TcpChannel(AioStreamChannel):

    def __init__(self, host, port):
        super(TcpChannel, self).__init__(
            None,
            None
        )
        self._host = host
        self._port = port

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(
            self._host,
            self._port
        )
