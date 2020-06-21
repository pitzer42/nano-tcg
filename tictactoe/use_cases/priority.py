from tictactoe.entities.match import TicTacToeMatch
from entities.player import Player
from tictactoe.repositories.match import MatchRepository

from tictactoe.adapters.client_channel import TicTacToeClientChannel as Client


async def has_priority(client: Client, player: Player, match: TicTacToeMatch, matches: MatchRepository, match_channel):
    match = await matches.get_by_id(match.id)
    await match_channel.receive()
    return match.priority == player.id
