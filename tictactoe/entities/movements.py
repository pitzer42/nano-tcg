from tictactoe.entities.player import Player


class Movement:

    def __init__(self, row, column):
        self._row = row
        self._column = column

    def apply(self, player: Player, match):
        match.board[self._row][self._column] = player.code
