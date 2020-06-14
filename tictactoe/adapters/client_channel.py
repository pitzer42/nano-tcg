import json
from typing import List

from channels import Channel
from tictactoe.entities.match import Match
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player
from tictactoe.use_cases.client import Client


class ClientChannel(Client, ):

    async def request_select_or_create_match(self) -> bool:
        request = dict(
            message='request_select_or_create_match',
            template=dict(option='select or create')
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['option'] == 'select'

    async def choose_one(self, options: List[Match]) -> Match:
        request = dict(
            message='choose_match',
            options=[m.to_dict() for m in options],
            template=dict(
                option_index=f'[0:{len(options) - 1}]'
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        index = response['option_index']
        return options[index]

    async def request_match_password(self, match: Match) -> str:
        request = dict(
            message='request_match_password',
            match=match.to_dict(),
            template=dict(
                password='plain_text'
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['password']

    async def alert_wrong_match_password(self, match: Match):
        request = dict(
            message='alert_wrong_match_password',
            match=match.to_dict()
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)

    async def request_new_match_id(self) -> str:
        request = dict(
            message='request_new_match_id',
            template=dict(
                match_id='plain_text'
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['match_id']

    async def request_new_match_password(self) -> str:
        request = dict(
            message='request_new_match_password',
            template=dict(
                password='plain_text'
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['password']

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

    async def choose_match(self, matches: List[Match]):
        request = dict(
            message='choose_match',
            options=[m.to_dict() for m in matches],
            template=dict(
                match_id='from options or new',
                password='plain text',
            )
        )
        json_request = json.dumps(request)
        await self._channel.send(json_request)
        json_response = await self._channel.receive()
        response = json.loads(json_response)
        return response['match_id'], response['password']

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
