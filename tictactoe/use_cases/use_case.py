from abc import ABC

from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.client import Client


class UseCase(ABC):

    def __init__(self,
                 client: Client,
                 match: Match,
                 player: Player,
                 matches: MatchRepository,
                 players: PlayerRepository):
        self.client = client
        self.matches = matches
        self.player = player
        self.match = match
        self.players = players

    async def execute(self, player_id, match_id):
        await self._fetch_entities(player_id, match_id)
        result = await self._execute()
        await self._update_repositories()
        await self._trace()
        return result

    async def _fetch_entities(self, player_id, match_id):
        self.player = await self.players.get_by_id(player_id)
        self.match = await self.matches.get_by_id(match_id)

    async def _execute(self):
        raise NotImplementedError()

    async def _update_repositories(self):
        await self.matches.save(self.match)
        await self.players.save(self.player)

    async def _trace(self):
        use_case_name = type(self).__name__
        player_id = self.player.id
        match_id = self.match.id
        trace_str = f'{use_case_name}(player={player_id}, match={match_id})'
        await self.match.channel.send(trace_str)
