from typing import List

from features.join_match.repositories import MatchAlreadyReadyException
from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository


class MemoryMatchRepository(MatchRepository):
    __memory__ = dict()

    def __init__(self, channel_factory):
        self.channel_factory = channel_factory

    async def get_by_id(self, match_id) -> Match:
        match = MemoryMatchRepository.__memory__.get(match_id)
        if match:
            match.channel = await self.channel_factory(match_id)
        return match

    async def create_match(self, match: Match):
        MemoryMatchRepository.__memory__[match.id] = match

    async def save(self, match: Match):
        MemoryMatchRepository.__memory__[match.id] = match

    async def all(self) -> List[Match]:
        return list(
            MemoryMatchRepository.__memory__.values()
        )

    async def get_waiting_matches(self) -> List[Match]:
        return [m for m in MemoryMatchRepository.__memory__.values() if not m.is_ready()]

    async def join(self, match: Match, player: Player):
        await match.join(player)
        await self.save(match)
        return match

    async def join_and_get_if_still_waiting(self, match: Match, player):
        match = await self.get_by_id(match.id)
        if match.is_ready():
            raise MatchAlreadyReadyException()
        match.join(player)
        return match


class MemoryPlayerRepository(PlayerRepository):
    __memory__ = dict()

    async def get_by_id(self, user_id) -> Player:
        return MemoryPlayerRepository.__memory__.get(user_id)

    async def save(self, user: Player):
        MemoryPlayerRepository.__memory__[user.id] = user

    async def all(self) -> List[Player]:
        return list(
            MemoryPlayerRepository.__memory__.values()
        )

    async def is_client_id_available(self, client_id):
        return client_id not in MemoryPlayerRepository.__memory__

    async def make_client_id_unavailable(self, client_id):
        MemoryPlayerRepository.__memory__[client_id] = client_id
