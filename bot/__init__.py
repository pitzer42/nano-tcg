from channel import TcpChannel

READ_FLAG = '$read'


class TestBot:

    def __init__(self, host, port):
        self._channel = TcpChannel.from_address(
            host,
            port
        )

    async def __aenter__(self):
        await self._channel.connect()
        return self

    async def send(self, *messages):
        responses = list()
        for message in messages:
            if message == READ_FLAG:
                response = await self._channel.receive()
                responses.append(response)
            else:
                await self._channel.send(message)
        return responses

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._channel.close()
