from abc import ABC
from typing import List

from features.select_match.entities import Match


class WaitingMatchRepository(ABC):
    async def get_waiting_matches(self) -> List[Match]:
        raise NotImplementedError()
