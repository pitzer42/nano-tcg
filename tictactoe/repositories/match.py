from typing import List

from features.join_match.repositories import JoinMatchRepository
from features.select_or_create_match.repositories import SelectOrCreateMatchRepository
from tictactoe.entities.match import Match
from tictactoe.entities.player import Player


class MatchRepository(SelectOrCreateMatchRepository, JoinMatchRepository):

    async def get_by_id(self, match_id) -> Match:
        raise NotImplementedError()

    async def save(self, match: Match):
        raise NotImplementedError()

    async def all(self) -> List[Match]:
        raise NotImplementedError()

    async def join(self, match: Match, player: Player):
        raise NotImplementedError()
