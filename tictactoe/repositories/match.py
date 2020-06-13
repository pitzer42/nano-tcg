from abc import ABC
from typing import List

from tictactoe.entities.match import Match
from tictactoe.entities.player import Player


class MatchRepository(ABC):

    async def get_by_id(self, match_id) -> Match:
        raise NotImplementedError()

    async def save(self, match: Match):
        raise NotImplementedError()

    async def all(self) -> List[Match]:
        raise NotImplementedError()

    async def all_waiting(self) -> List[Match]:
        raise NotImplementedError()

    async def join(self, match: Match, player: Player):
        raise NotImplementedError()
