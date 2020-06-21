from typing import Tuple, List

from adapters import messages
from channels import Channel
from channels.decorators.json import JsonChannel
from entities.match import Match
from entities.player import Player
from features.identify_client.clients import IdentifiableClient
from features.basic_onboard.join_match.clients import JoinMatchClient
from features.basic_onboard.select_or_create_match.clients import SelectOrCreateMatchClient
from features.sync.clients import SyncClient


class ClientChannel(JsonChannel, IdentifiableClient, SelectOrCreateMatchClient, JoinMatchClient, SyncClient):

    def __init__(self, base_channel: Channel):
        JsonChannel.__init__(self, base_channel)

    async def request_client_id(self) -> str:
        await self.send(message=messages.request_client_id)
        response = await self.receive()
        return response[messages.client_id]

    async def request_match_id_and_password(self, waiting_matches: List[Match]) -> Tuple[str, str]:
        await self.send(
            message=messages.request_match_id_and_password,
            options=[m.to_dict() for m in waiting_matches],
        )
        response = await self.receive()
        return (
            response[messages.match_id],
            response[messages.password]
        )

    async def alert_wrong_match_password(self, match: Match):
        await self.send(
            message=messages.alert_wrong_match_password,
            match=match.to_dict()
        )

    async def sync(self, player: Player, match: Match):
        await self.send(
            messages=messages.sync,
            player=player.to_dict(),
            match=match.to_dict()
        )

