from functools import partial
from entities.player import Player
from features.game_loop.feature import GameLoop
from features.onboard.feature import Onboard
from features.sync.feature import Sync
from tictactoe.adapters.client_channel import TicTacToeClientChannel
from tictactoe.adapters.match_channel import TicTacToeMatchClient
from tictactoe.entities.match import TicTacToeMatch
from tictactoe.repositories.match import TicTacToeMatchRepository
from tictactoe.repositories.player import TicTacToePlayerRepository
from tictactoe.use_cases.play import Play


class TicTacToeGameLoop:

    def __init__(self,
                 player_client: TicTacToeClientChannel,
                 player_repo: TicTacToePlayerRepository,
                 match_repo: TicTacToeMatchRepository,
                 match_client_factory):

        self.player_client = player_client

        def create_game_loop(match_channel):
            return GameLoop(
                match_channel,
                Sync(player_client),
                Play(
                    player_client,
                    match_repo
                )
            )

        self.create_game_loop = create_game_loop

        self.onboard = Onboard(
            player_client,
            Player,
            player_repo,
            TicTacToeMatch,
            match_repo,
            match_client_factory
        )

    async def execute(self):
        player, match, match_channel = await self.onboard.execute()
        loop = self.create_game_loop(match_channel)
        await loop.execute(player, match)
        await self.player_client.notify_game_over(match.winner())
        await self.player_client.close()
        await match_channel.close()
