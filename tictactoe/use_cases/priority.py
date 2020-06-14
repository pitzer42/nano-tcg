from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.use_cases.client import Client


async def has_priority(client: Client, player: Player, match: Match, matches: MatchRepository, match_channel):
    match = await matches.get_by_id(match.id)
    await match_channel.receive()
    return match.current_player == player.id
