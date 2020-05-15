from typing import List

from channels import Channel


class Player:

    def __init__(self, channel: Channel, player_id: str):
        self.id = player_id
        self.deck: List[str] = list()
        self.hand: List[str] = list()
        self.board: List[str] = list()
