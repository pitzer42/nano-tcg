from gloop.entities.player import Player


class Movement:

    def __init__(self, row, column):
        self._row = row
        self._column = column

    def apply(self, player: Player, match):
        match.board[self._row][self._column] = player.id

    def to_dict(self):
        return dict(
            row=self._row,
            column=self._column
        )
