import json
from typing import List

from gloop.adapters.client_channel import PlayerClientChannel
from tictactoe.entities.match import TicTacToeMatch
from tictactoe.entities.movements import Movement


class TicTacToeClientChannel(PlayerClientChannel):

    def __init__(self, inner_channel):
        super(TicTacToeClientChannel, self).__init__(inner_channel)

    async def alert_match_creation_exception(self, exception):
        request = dict(
            message='alert_match_creation_exception',
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)

    async def winner(self):
        request = dict(
            message='you won!'
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)

    async def loser(self):
        request = dict(
            message='you lost...'
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)

    async def draw(self):
        request = dict(
            message='draw'
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)

    async def failed_to_join_match(self, match: TicTacToeMatch):
        request = dict(
            message='failed_to_join_match',
            match_id=match.id
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)

    async def request_move(self, options: List[Movement]):
        request = dict(
            message='request_move',
            options=[m.to_dict() for m in options],
            template=dict(
                movement_index=f'[0:{len(options) - 1}]'
            )
        )
        json_request = json.dumps(request)
        await self.inner_channel.send(json_request)
        json_response = await self.inner_channel.receive()
        response = json.loads(json_response)
        movement_index = int(response['movement_index'])
        return options[movement_index]

    async def notify_game_over(self, winner):
        message = dict(
            message='notify_game_over',
            winner=winner
        )
        json_message = json.dumps(message)
        await self.inner_channel.send(json_message)
