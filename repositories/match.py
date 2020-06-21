from abc import ABC


class MatchRepository(ABC):
    async def insert_match(self, match):
        raise NotImplementedError()
