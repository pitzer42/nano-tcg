from abc import ABC
from typing import List

from entities.match import Match


class SelectOrCreateMatchRepository(ABC):
    async def get_waiting_matches(self) -> List[Match]:
        raise NotImplementedError()

    async def create_match(self, match):
        raise NotImplementedError()


class CreateMatchException(Exception):
    pass
