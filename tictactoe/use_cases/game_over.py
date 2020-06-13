from tictactoe.entities.match import Match
from tictactoe.repositories.match import MatchRepository


async def game_over(match: Match, matches: MatchRepository):
    match = await matches.get_by_id(match.id)
    return match.game_over()

