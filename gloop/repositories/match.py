from abc import ABC
from typing import List

from gloop.entities.match import Match


class MatchRepository(ABC):

    async def get_match_by_id(self, match_id) -> Match:
        raise NotImplementedError()

    async def insert_match(self, match):
        raise NotImplementedError()

    async def get_waiting_matches(self) -> List[Match]:
        raise NotImplementedError()

    async def join_if_still_waiting(self, player, match):
        raise NotImplementedError()
