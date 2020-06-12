from channels import Channel


class Sync:

    def __init__(self, channel: Channel, serialize, deserialize):
        self._channel = channel
        self.serialize = serialize
        self.deserialize = deserialize

    async def push(self, state):
        message = self.serialize(state)
        await self._channel.send(message)

    async def pull(self):
        message = await self._channel.receive()
        state = self.deserialize(message)
        return state
