import json

from channels import Channel


class JsonChannel(Channel):

    def __init__(self, inner_channel: Channel):
        self.inner_channel = inner_channel

    async def connect(self):
        await self.inner_channel.connect()

    async def send(self, **message):
        json_message = json.dumps(message)
        await self.inner_channel.send(json_message)

    async def receive(self) -> dict:
        json_message = await self.inner_channel.receive()
        return json.loads(json_message)

    async def close(self):
        await self.inner_channel.close()
