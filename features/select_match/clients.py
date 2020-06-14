from abc import ABC
from typing import List

from features.select_match.entities import Match


class SelectMatchClient(ABC):
    async def choose_one(self, options: List[Match]) -> Match:
        raise NotImplementedError()

    async def request_match_password(self, match: Match) -> str:
        raise NotImplementedError()

    async def alert_wrong_match_password(self, match: Match):
        raise NotImplementedError()
