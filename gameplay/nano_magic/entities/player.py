from typing import List

from channels import Channel


class Player(Channel):

    def __init__(self, channel: Channel, player_id: str):
        self.channel = channel
        self.id = player_id
        self.deck: List[str] = list()
        self.hand: List[str] = list()

    async def connect(self):
        await self.channel.connect()

    async def send(self, message: str):
        return await self.channel.send(message)

    async def receive(self) -> str:
        return await self.channel.receive()

    async def close(self):
        return await self.channel.close()
