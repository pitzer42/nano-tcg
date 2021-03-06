from asyncio import Event
from asyncio import Lock
from asyncio import sleep
from typing import List
from gloop.channels import Channel

from nano_magic.entities.player import Player


class Match:
    PLAYERS_IN_MATCH = 2

    def __init__(self, match_id: str, password: str, channel: Channel):
        self.id = match_id
        self.password = password
        self.players: List[Player] = list()
        self.board: List = list()
        self._channel = channel
        self._is_ready = False
        self._to_be_ready: Event = Event()
        self._turn_index = 0
        self._to_be_turn: Lock = Lock()

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

    async def next_turn(self):
        self._turn_index = 1 - self._turn_index
        self._to_be_turn.release()

    async def to_be_turn(self, player_index: int):
        while self._turn_index != player_index:
            await sleep(1)
        await self._to_be_turn.acquire()
