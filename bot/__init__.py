import asyncio

from bot import lang


class ClientBot:

    def __init__(self):
        self._input = None
        self._output = None
        self._logs = list()
        self._program = list()

    def set_instructions(self, instructions):
        self._program = lang.compile_commands(instructions)

    async def connect(self, host, port):
        self._input, self._output = await asyncio.open_connection(
            host,
            port
        )

        assert self._input is not None
        assert self._output is not None

    async def run(self):
        logs = list()
        for command in self._program:
            if command == lang.compiled_read_command:
                response = await self._input.readline()
                logs.append(response)
            else:
                self._output.write(command)
                await self._output.drain()

        return logs

    async def close(self):
        self._output.close()
        await self._output.wait_closed()
