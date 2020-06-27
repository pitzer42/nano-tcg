from entities.player import Player
from tictactoe.adapters.client_channel import TicTacToeClientChannel as Client
from tictactoe.entities.match import TicTacToeMatch
from tictactoe.repositories.match import MatchRepository, TicTacToeMatchRepository


class Play:

    def __init__(self, client: Client, matches: TicTacToeMatchRepository):
        self.client = client
        self.matches = matches

    async def execute(self, player: Player, match: TicTacToeMatch):
        possible_moves = match.get_possible_moves()
        move = await self.client.request_move(possible_moves)
        move.apply(player, match)
        await self.matches.insert_match(match)
        match.yield_priority()
