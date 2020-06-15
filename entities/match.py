import json
from typing import List


class Match:
    SIZE = 2

    def __init__(self, match_id, password, channel):
        self.match_id = match_id
        self.password = password
        self.channel = channel
        self.players: List = list()

    def join(self, player):
        if self.is_ready():
            return False
        self.players.append(player)
        return True

    def is_ready(self) -> bool:
        return len(self.players) == Match.SIZE

    async def notify_is_ready(self):
        message = dict(
            message='ready'
        )
        json_message = json.dumps(message)
        await self.channel.send(json_message)
