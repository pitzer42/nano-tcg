from nano_magic.entities.match import Match
from nano_magic.repositories.match import MatchRepository


class MemoryMatchRepository(MatchRepository):
    __memory__ = dict()

    async def get_by_id(self, match_id) -> Match:
        return MemoryMatchRepository.__memory__.get(match_id)

    async def save(self, match: Match):
        MemoryMatchRepository.__memory__[match.id] = match
