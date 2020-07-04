from abc import ABC

from gloop.entities.match import Match
from gloop.entities.player import Player


class MatchClient(ABC):

    async def wait_notification(self):
        raise NotImplementedError()

    async def notify_new_player_join(self, player: Player):
        raise NotImplementedError()

    async def notify_match_start(self, match: Match):
        raise NotImplementedError()

    async def notify_play(self, player: Player):
        raise NotImplementedError()

    async def notify_game_over(self, match: Match):
        raise NotImplementedError()
