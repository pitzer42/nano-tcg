import json
from typing import List, Tuple

from channels import Channel
from tictactoe.entities.match import Match
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player
from tictactoe.use_cases.client import Client


class ClientChannel(Client):

    async def request_match_id_and_password(self, options: List[Match]) -> Tuple[str, str]:
        request = dict(
            message='request_match_id_and_password',
            options=[m.to_dict() for m in options],
            template=dict(
                match_id='str',
                password='str',
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['match_id'], response['password']

    async def alert_wrong_match_password(self, match: Match):
        request = dict(
            message='alert_wrong_match_password',
            match=match.to_dict()
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def alert_match_creation_exception(self, exception):
        request = dict(
            message='alert_match_creation_exception',
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def winner(self):
        request = dict(
            message='you won!'
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def loser(self):
        request = dict(
            message='you lost...'
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def draw(self):
        request = dict(
            message='draw'
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    def __init__(self, channel: Channel):
        self._channel = channel

    async def request_client_id(self):
        request = dict(
            message='request_player_id',
            template=dict(player_id='foo')
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['player_id']

    async def failed_to_join_match(self, match: Match):
        request = dict(
            message='failed_to_join_match',
            match_id=match.id
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def sync(self, player: Player, match: Match):
        request = dict(
            message='sync',
            match=match.to_dict()
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def request_move(self, options: List[Movement]):
        request = dict(
            message='request_move',
            options=[m.to_dict() for m in options],
            template=dict(
                movement_index=f'[0:{len(options) - 1}]'
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        movement_index = int(response['movement_index'])
        return options[movement_index]
