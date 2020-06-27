from entities.match import Match
from tictactoe.entities.movements import Movement


class TicTacToeMatch(Match):
    EMPTY = '*'

    def __init__(self, match_id, password):
        super(TicTacToeMatch, self).__init__(
            match_id,
            password)
        self.board = [
            [TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY],
            [TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY],
            [TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY, TicTacToeMatch.EMPTY],
        ]

    def get_possible_moves(self):
        movements = list()
        for row, column in self._available_cells():
            movements.append(Movement(row, column))
        return movements

    def _available_cells(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if self.board[i][j] == TicTacToeMatch.EMPTY:
                    yield i, j

    def game_over(self) -> bool:
        for player in self.players:
            player_id = player.id
            winning_row = [player_id, player_id, player_id]
            if winning_row in self.board:
                return player_id

            diagonal_a = 0
            diagonal_b = 0
            for i in range(3):
                if self.board[i][i] == player_id:
                    diagonal_a += 1
                if self.board[i][2 - i] == player_id:
                    diagonal_b += 1
            if 3 in (diagonal_a, diagonal_b):
                return player_id

            for j in range(3):
                vertical = 0
                for i in range(3):
                    if self.board[i][j] == player_id:
                        vertical += 1
                if vertical == 3:
                    return player_id

        if len(list(self._available_cells())) == 0:
            return 'draw'

        return False

    def winner(self):
        return self.game_over()

    def to_dict(self) -> dict:
        _dict = super(TicTacToeMatch, self).to_dict()
        _dict['board'] = self.board
        return _dict
