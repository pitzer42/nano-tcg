from entities.match import Match
from entities.player import Player
from features.sync.clients import SyncClient


class Sync:

    def __init__(self, client: SyncClient):
        self.client = client

    async def execute(self, player: Player, match: Match):
        await self.client.sync(player, match)
