from features.basic_onboard.feature import BasicOnboard
from features.identify_client.feature import IdentifyClient
from features.basic_onboard.join_match.feature import JoinMatch
from features.basic_onboard.select_or_create_match.feature import SelectOrCreateMatch
from features.game_loop.feature import GameLoop
from features.sync.feature import Sync
from tictactoe.adapters.client_channel import TicTacToeClientChannel
from tictactoe.entities.match import TicTacToeMatch
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.play import Play


class TicTacToeGameLoop:

    def __init__(self,
                 client_channel: TicTacToeClientChannel,
                 match_channel_factory,
                 players: PlayerRepository,
                 matches: MatchRepository):
        self.client_channel = client_channel
        self.players = players
        self.matches = matches

        self.onboard = BasicOnboard(
            IdentifyClient(
                client_channel,
                players
            ),
            SelectOrCreateMatch(
                client_channel,
                matches,
                TicTacToeMatch,
                match_channel_factory
            ),
            JoinMatch(
                client_channel,
                matches
            )
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
