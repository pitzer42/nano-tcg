from gloop.clients.match import MatchClient
from gloop.features.sync.feature import Sync


class GameLoop:

    def __init__(self,
                 match_client: MatchClient,
                 sync: Sync,
                 play):
        self.match_client = match_client
        self.sync = sync
        self.play = play

    async def execute(self, player, match):
        while True:
            await self.sync.execute(player, match)
            await self.match_client.wait_notification()
            await self.sync.execute(player, match)
            if match.has_priority(player):
                if match.game_over():
                    break
                await self.play.execute(player, match)
                await self.match_client.notify_play(player)
                if match.game_over():
                    break
        await self.sync.execute(player, match)
        await self.match_client.notify_game_over(match)
