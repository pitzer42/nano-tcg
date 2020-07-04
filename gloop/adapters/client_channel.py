from gloop.adapters import messages
from gloop.channels import Channel
from gloop.channels.decorators.json import JsonChannel
from gloop.clients.player import PlayerClient
from gloop.entities.match import Match
from gloop.entities.player import Player


class PlayerClientChannel(JsonChannel, PlayerClient):

    def __init__(self, base_channel: Channel):
        super(PlayerClientChannel, self).__init__(base_channel)

    async def request_player_id(self):
        await self.send(message=messages.request_client_id)
        response = await self.receive()
        return response[messages.client_id]

    async def request_match_id_and_password(self, waiting_matches):
        await self.send(
            message=messages.request_match_id_and_password,
            options=[m.to_dict() for m in waiting_matches],
        )
        response = await self.receive()
        return (
            response[messages.match_id],
            response[messages.password]
        )

    async def notify_unavailable_player_id(self, player_id):
        await self.send(
            message=messages.alert_unavailable_player_id,
            player_id=player_id
        )

    async def notify_match_has_already_started(self, match):
        await self.send(
            message=messages.alert_match_has_already_started,
            match=match.to_dict()
        )

    async def sync(self, player: Player, match: Match):
        await self.send(
            message=messages.sync,
            player=player.to_dict(),
            match=match.to_dict()
        )
