from asyncio import Event
from typing import List

from nano_magic.entities.player import Player


class Match:
    PLAYERS_IN_MATCH = 2

    def __init__(self, match_id: str, password: str):
        self.id = match_id
        self.password = password
        self.players: List[Player] = list()
        self._is_ready = False
        self._to_be_ready: Event = Event()

    @property
    def is_ready(self):
        return self._is_ready

    async def to_be_ready(self):
        await self._to_be_ready.wait()

    def join(self, player: Player):
        self.players.append(player)
        n_players = len(self.players)
        if n_players == Match.PLAYERS_IN_MATCH:
            self._is_ready = True
            self._to_be_ready.set()
        return n_players - 1  # player index

    def check_password(self, password):
        return self.password == password
