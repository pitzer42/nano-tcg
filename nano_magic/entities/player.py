from typing import List


class Player:

    def __init__(self, player_id: str):
        self.id = player_id
        self.deck: List[str] = list()
        self.hand: List[str] = list()
        self.board: List[str] = list()
        self.resources: dict = dict()
