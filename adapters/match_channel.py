from adapters import messages
from channels import Channel
from channels.decorators.json import JsonChannel
from clients.match_client import MatchClient


class MatchClientChannel(JsonChannel, MatchClient):

    def __init__(self, inner_channel: Channel):
        super(MatchClientChannel, self).__init__(inner_channel)

    async def notify_new_player_join(self, player):
        await self.inner_channel.send(
            message=messages.notify_new_player_join,
            player=player.to_dict()
        )

    async def notify_match_start(self, match):
        await self.inner_channel.send(
            message=messages.notify_match_start,
            match=match.to_dict()
        )
