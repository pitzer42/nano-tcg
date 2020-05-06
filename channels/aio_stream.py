from channels import Channel


class AioStreamChannel(Channel):

    def __init__(self, reader, writer):
        super(AioStreamChannel, self).__init__()
        self._reader = reader
        self._writer = writer

    async def connect(self):
        pass

    async def send(self, message: str):
        message_bytes = (str(message) + '\n').encode()
        self._writer.write(message_bytes)
        await self._writer.drain()

    async def receive(self) -> str:
        message_bytes = await self._reader.readline()
        if len(message_bytes) == 0:
            raise ConnectionAbortedError()
        return message_bytes.decode().strip()

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()
