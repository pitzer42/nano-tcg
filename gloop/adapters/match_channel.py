from gloop.adapters import messages
from gloop.channels import Channel
from gloop.channels.decorators.json import JsonChannel
from gloop.clients.match import MatchClient
from gloop.entities.match import Match
from gloop.entities.player import Player


class MatchClientChannel(JsonChannel, MatchClient):

    def __init__(self, inner_channel: Channel):
        super(MatchClientChannel, self).__init__(inner_channel)

    async def wait_notification(self):
        await self.receive()

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

    async def notify_play(self, player: Player):
        await self.send(
            message=messages.notify_play,
            player_id=player.id
        )

    async def notify_game_over(self, match: Match):
        await self.send(
            message=messages.notify_game_over
        )
