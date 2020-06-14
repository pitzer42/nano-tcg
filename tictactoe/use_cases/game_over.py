from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.use_cases.client import Client


async def game_over(match: Match, matches: MatchRepository, client: Client, player: Player):
    match = await matches.get_by_id(match.id)
    winner = match.game_over()
    if winner:
        if winner == player.id:
            await client.winner()
        elif winner == 'draw':
            await client.draw()
        else:
            await client.loser()
    return winner
