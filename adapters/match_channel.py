from adapters import messages
from channels import Channel
from channels.decorators.json import JsonChannel
from clients.match_client import MatchClient
from entities.match import Match
from entities.player import Player


class MatchClientChannel(JsonChannel, MatchClient):

    def __init__(self, inner_channel: Channel):
        super(MatchClientChannel, self).__init__(inner_channel)

    async def wait_notification(self):
        await self.receive()

    async def notify_play(self, player: Player):
        await self.send(
            message=messages.notify_play,
            player_id=player.id
        )

    async def notify_game_over(self, match: Match):
        await self.send(
            message=messages.notify_game_over
        )

    async def notify_new_player_join(self, player):
        await self.send(
            message=messages.notify_new_player_join,
            player=player.to_dict()
        )

    async def notify_match_start(self, match):
        await self.send(
            message=messages.notify_match_start,
            match=match.to_dict()
        )
