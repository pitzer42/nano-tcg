from typing import List


class Match:
    SIZE = 2

    def __init__(self, match_id, password):
        self.id = match_id
        self.check_password = lambda a: a == password
        self.players: List = list()
        self.priority = None
        self._priority_index = None

    def join(self, player):
        if self.is_ready():
            return False
        self.players.append(player)
        return True

    def is_ready(self) -> bool:
        return len(self.players) == Match.SIZE

    def has_priority(self, player):
        return self.priority is not None and self.priority.id == player.id

    def yield_priority(self):
        if self._priority_index is None:
            self._priority_index = 0
        else:
            self._priority_index += 1
            if self._priority_index == len(self.players):
                self._priority_index = 0
        self.priority = self.players[self._priority_index]

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            is_ready=self.is_ready()
        )
