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

        loop = GameLoop(
            match_channel,
            Sync(
                self.client_channel
            ),
            Play(
                self.client_channel,
                self.matches
            )
        )

        await loop.execute(player, match)

        await self.client_channel.close()
        await match_channel.close()
