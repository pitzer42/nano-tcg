from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository


async def join(player: Player, match: Match, matches: MatchRepository):
    updated_match = await matches.join(match, player)
    if updated_match:
        await updated_match.channel.send(player.id)
    return updated_match
