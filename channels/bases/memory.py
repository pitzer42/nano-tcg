import asyncio

from channels import Channel


class MemoryChannel(Channel):
    memory = dict()

    def __init__(self, topic_name='default'):
        super(MemoryChannel, self).__init__()
        self._topic_name = topic_name
        self._head = 0
        self._topic = None

    async def connect(self):
        if self._topic_name not in MemoryChannel.memory:
            MemoryChannel.memory[self._topic_name] = list()
        self._topic = MemoryChannel.memory[self._topic_name]

    async def close(self):
        await self._ws.close()

    async def send(self, message: str):
        self._topic.append(message)
        self._head += 1

    async def receive(self) -> str:
        while len(self._topic) <= self._head:
            await asyncio.sleep(1)
        message = self._topic[self._head]
        self._head += 1
        return message
