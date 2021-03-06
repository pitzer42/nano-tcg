from abc import ABC
from typing import List

from nano_magic.entities.match import Match


class MatchRepository(ABC):

    async def get_by_id(self, match_id) -> Match:
        raise NotImplementedError()

    async def save(self, match: Match):
        raise NotImplementedError()

    async def all(self) -> List[Match]:
        raise NotImplementedError()
