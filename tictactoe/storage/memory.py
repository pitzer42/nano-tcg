from typing import List

from entities.player import Player
from features.basic_onboard.join_match.repositories import MatchAlreadyReadyException
from tictactoe.entities.match import TicTacToeMatch
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository


class MemoryMatchRepository(MatchRepository):
    __memory__ = dict()

    async def get_by_id(self, match_id) -> TicTacToeMatch:
        match = MemoryMatchRepository.__memory__.get(match_id)
        if match:
            _copy = TicTacToeMatch(match_id, None)
            _copy.check_password = match.check_password
            _copy.board = match.board
            _copy.players = match.players
            _copy.priority = match.priority
            _copy._priority_index = match._priority_index
        return match

    async def save_match(self, match: TicTacToeMatch):
        MemoryMatchRepository.__memory__[match.id] = match

    async def save(self, match: TicTacToeMatch):
        MemoryMatchRepository.__memory__[match.id] = match

    async def all(self) -> List[TicTacToeMatch]:
        return list(
            MemoryMatchRepository.__memory__.values()
        )

    async def get_waiting_matches(self) -> List[TicTacToeMatch]:
        return [m for m in MemoryMatchRepository.__memory__.values() if not m.is_ready()]

    async def join(self, match: TicTacToeMatch, player: Player):
        await match.join(player)
        await self.save(match)
        return match

    async def join_and_get_if_still_waiting(self, match: TicTacToeMatch, player):
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
