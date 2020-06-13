from abc import ABC
from typing import List
from typing import Tuple

from channels import Channel
from tictactoe.entities.match import Match
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player


class Client(ABC):

    def __init__(self, channel: Channel):
        self._channel = channel

    async def request_player_id(self):
        raise NotImplementedError()

    async def choose_match(self, matches: List[Match]) -> Tuple[str, str]:
        raise NotImplementedError()

    async def failed_to_join_match(self, match: Match):
        raise NotImplementedError()

    async def sync(self, player: Player, match: Match):
        raise NotImplementedError()

    async def request_move(self, options: List[Movement]):
        raise NotImplementedError()
