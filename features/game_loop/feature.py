from features.game_loop.clients import BaseMatchClient
from features.sync.feature import Sync


class GameLoop:

    def __init__(self, match_client: BaseMatchClient, sync: Sync, play):
        self.match_client = match_client
        self.sync = sync
        self.play = play

    async def execute(self, player, match):

        game_over = False

        while not game_over:

            await self.sync.execute(player, match)
            print(f'{player.id} has {self.match_client.inner_channel}')
            await self.match_client.wait_update()
            await self.sync.execute(player, match)

            if match.has_priority(player):

                game_over = match.game_over()
                if game_over:
                    break

                await self.play.execute(player, match)
                await self.match_client.update()

                game_over = match.game_over()
                if game_over:
                    break
