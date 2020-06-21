from tictactoe.entities.match import TicTacToeMatch
from entities.player import Player
from tictactoe.repositories.match import MatchRepository

from tictactoe.adapters.client_channel import TicTacToeClientChannel as Client


async def game_over(match: TicTacToeMatch, matches: MatchRepository, client: Client, player: Player):
    match = await matches.get_by_id(match.id)
    winner = match.game_over()
    if winner:
        if winner == player.id:
            await client.winner()
        elif winner == 'draw':
            await client.draw()
        else:
            await client.loser()
        await match.update()
    return winner
