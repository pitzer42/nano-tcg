from abc import ABC
from typing import List
from typing import Tuple

from channels import Channel
from features.create_match.clients import CreateMatchClient
from features.indentify_client.clients import IdentifiableClient
from features.select_match.clients import SelectMatchClient
from features.select_or_create_match.clients import SelectOrCreateMatchClient
from tictactoe.entities.match import Match
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player


class Client(IdentifiableClient, SelectOrCreateMatchClient, SelectMatchClient, CreateMatchClient):

    def __init__(self, channel: Channel):
        self._channel = channel

    async def choose_match(self, matches: List[Match]) -> Tuple[str, str]:
        raise NotImplementedError()

    async def failed_to_join_match(self, match: Match):
        raise NotImplementedError()

    async def sync(self, player: Player, match: Match):
        raise NotImplementedError()

    async def request_move(self, options: List[Movement]):
        raise NotImplementedError()

    async def winner(self):
        raise NotImplementedError()

    async def loser(self):
        raise NotImplementedError()

    async def draw(self):
        raise NotImplementedError()
