from asyncio import Event
from typing import List

from gameplay.nano_magic.entities.player import Player


class Match:
    PLAYERS_IN_MATCH = 2

    def __init__(self, match_id: str, password: str):
        self.id = match_id
        self.password = password
        self.players: List[Player] = list()
        self._is_ready: Event = Event()

    def join(self, player: Player):
        self.players.append(player)
        n_players = len(self.players)
        if n_players == Match.PLAYERS_IN_MATCH:
            self._is_ready.set()
        return n_players - 1  # player index

    async def is_ready(self):
        await self._is_ready.wait()
