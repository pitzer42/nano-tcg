from channels import Channel


class AioStreamChannel(Channel):

    def __init__(self, reader, writer):
        super(AioStreamChannel, self).__init__()
        self._reader = reader
        self._writer = writer

    async def connect(self):
        pass

    async def _send(self, packet: bytes):
        self._writer.write(packet)
        await self._writer.drain()

    async def _receive(self) -> bytes:
        packet = await self._reader.readline()
        if len(packet) == 0:
            raise ConnectionAbortedError()
        return packet

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()