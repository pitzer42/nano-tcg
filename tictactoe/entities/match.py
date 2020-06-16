from channels import Channel
from entities.match import Match as BaseMatch
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player


class Match(BaseMatch):
    SIZE = 2

    def __init__(self, match_id, password, channel: Channel):
        super(Match, self).__init__(
            match_id,
            password,
            channel)
        self.board = [['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*']]
        self.current_player = None

    def join(self, player):
        success = super(Match, self).join(player)
        if self.is_ready():
            self.current_player = self.players[0].id
        return success

    def get_possible_moves(self, player: Player):
        movements = list()
        for row, column in self._get_available_cells():
            movements.append(Movement(row, column))
        return movements

    def _get_available_cells(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if self.board[i][j] == '*':
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

        if len(list(self._get_available_cells())) == 0:
            return 'draw'

        return False

    def to_dict(self):
        return dict(
            match_id=self.id,
            remaining_players=Match.SIZE - len(self.players),
            board=self.board
        )