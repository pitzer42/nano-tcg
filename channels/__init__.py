import asyncio
from modes.nano_magic import protocol


class TcpChannel:

    @staticmethod
    def from_address(host, port):
        return TcpChannel(host, port, None, None)

    @staticmethod
    def from_stream(reader, writer):
        return TcpChannel(None, None, reader, writer)

    def __init__(self, host, port, reader, writer):
        self._host = host
        self._port = port
        self._reader = reader
        self._writer = writer

    async def __aenter__(self):
        await self.connect()
        return self

    async def connect(self):
        if self._reader is None and self._writer is None:
            self._reader, self._writer = await asyncio.open_connection(
                self._host,
                self._port
            )

        assert self._reader is not None
        assert self._writer is not None

    async def send(self, message: str):
        packet = protocol.pack(message)
        self._writer.write(packet)
        await self._writer.drain()

    async def receive(self) -> str:
        response = await self._reader.readline()
        if len(response) == 0:
            raise ConnectionAbortedError()
        return protocol.unpack(response)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

