from typing import List

from features.basic_onboard.join_match.repositories import JoinMatchRepository
from features.basic_onboard.select_or_create_match.repositories import SelectOrCreateMatchRepository
from tictactoe.entities.match import TicTacToeMatch
from entities.player import Player


class MatchRepository(SelectOrCreateMatchRepository, JoinMatchRepository):

    async def get_by_id(self, match_id) -> TicTacToeMatch:
        raise NotImplementedError()

    async def save(self, match: TicTacToeMatch):
        raise NotImplementedError()

    async def all(self) -> List[TicTacToeMatch]:
        raise NotImplementedError()

    async def join(self, match: TicTacToeMatch, player: Player):
        raise NotImplementedError()
