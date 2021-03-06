from gloop.entities.match import Match
from gloop.entities.player import Player


class SyncClient:

    async def sync(self, player: Player, match: Match):
        raise NotImplementedError()
