import asyncio
import protocol


READ_FLAG = '$read'
WRAPPED_READ_FLAG = protocol.wrap_message(READ_FLAG)


class TelnetBot:

    def __init__(self, host, port):
        self._host = host
        self._port = port

        self._input = None
        self._output = None
        self._logs = list()
        self._program = list()

    async def __aenter__(self):
        await self.connect()
        return self

    async def connect(self):
        self._input, self._output = await asyncio.open_connection(
            self._host,
            self._port
        )

        assert self._input is not None
        assert self._output is not None

    async def send(self, *messages):
        responses = list()
        for message in messages:
            wrapped_message = protocol.wrap_message(message)
            # TODO: timeout
            if wrapped_message == WRAPPED_READ_FLAG:
                response = await self._input.readline()
                responses.append(response)
            else:
                self._output.write(wrapped_message)
                await self._output.drain()
        return responses

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        self._output.close()
        await self._output.wait_closed()
