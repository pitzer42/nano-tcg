from channels import Channel
from features.identify_client.clients import IdentifiableClient
from features.join_match.client import JoinMatchClient
from features.select_or_create_match.clients import SelectOrCreateMatchClient


class Client(IdentifiableClient, SelectOrCreateMatchClient, JoinMatchClient):

    def __init__(self, channel: Channel):
        self._channel = channel

    async def close(self):
        await self._channel.close()
