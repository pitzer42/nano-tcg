from adapters import messages
from channels import Channel
from channels.decorators.json import JsonChannel
from features.game_loop.clients import BaseMatchClient


class MatchChannel(JsonChannel, BaseMatchClient):

    def __init__(self, inner_channel: Channel):
        super(MatchChannel, self).__init__(inner_channel)

    async def wait_update(self):
        print(f'waiting on {self.inner_channel}')
        await self.inner_channel.receive()

    async def update(self):
        print(f'updating from {self.inner_channel}')
        await self.inner_channel.send(message=messages.match_update)
