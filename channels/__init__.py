import asyncio

from modes.nano_magic import protocol


class Channel:

    async def __aenter__(self):
        await self.connect()
        return self

    async def connect(self):
        raise NotImplementedError()

    async def send(self, message: str):
        packet = protocol.pack(message)
        return await self._send(packet)

    async def receive(self) -> str:
        packet = await self._receive()
        return protocol.unpack(packet)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        raise NotImplementedError()
