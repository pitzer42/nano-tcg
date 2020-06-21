from tictactoe.repositories.match import TicTacToeMatchRepository
from tictactoe.repositories.player import TicTacToePlayerRepository


class TicTacToeMatchMemoryRepository(TicTacToeMatchRepository):
    __memory__ = dict()

    async def get_match_by_id(self, match_id):
        return TicTacToeMatchMemoryRepository.__memory__.get(match_id)

    async def insert_match(self, match):
        TicTacToeMatchMemoryRepository.__memory__[match.id] = match

    async def get_waiting_matches(self):
        return [m for m in TicTacToeMatchMemoryRepository.__memory__.values() if not m.is_ready()]

    async def join_if_still_waiting(self, player, match):
        if match.is_ready():
            return False
        match.join(player)
        TicTacToeMatchMemoryRepository.__memory__[match.id] = match


class TicTacToePlayerMemoryRepository(TicTacToePlayerRepository):
    __memory__ = dict()

    async def make_player_id_unavailable_if_is_available(self, player_id) -> bool:
        if player_id in TicTacToePlayerMemoryRepository.__memory__:
            return False
        TicTacToePlayerMemoryRepository.__memory__[player_id] = True
        return True
