from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.use_cases.client import Client


async def play(client: Client, player: Player, match: Match):
    possible_moves = match.get_possible_moves(player)
    move = await client.request_move(possible_moves)
    move.apply(player, match)
