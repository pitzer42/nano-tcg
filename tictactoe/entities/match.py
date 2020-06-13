from channels import Channel
from tictactoe.entities.movements import Movement
from tictactoe.entities.player import Player


class Match:
    SIZE = 2

    def __init__(self, match_id, password, channel: Channel):
        self.id = match_id
        self.players = list()
        self.channel = channel
        self.check_password = lambda a: a == password
        self.board = [['*'] * 3] * 3
        self.current_player = None

    async def join(self, player):
        if self.is_ready():
            return False
        self.players.append(player)
        if self.is_ready():
            self.current_player = self.players[0].id

    def is_ready(self) -> bool:
        return len(self.players) == Match.SIZE

    def get_possible_moves(self, player: Player):
        movements = list()
        for row, column in self._get_available_cells():
            movements.append(Movement(row, column))

    def _get_available_cells(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if self.board[i][j] == '*':
                    yield i, j

    def game_over(self) -> bool:
        return False

    def to_dict(self):
        return dict(
            match_id=self.id,
            remaining_players=Match.SIZE - len(self.players)
        )
