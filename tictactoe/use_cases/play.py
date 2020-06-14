from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.use_cases.client import Client


async def play(client: Client, player: Player, match: Match, match_channel, matches: MatchRepository):
    possible_moves = match.get_possible_moves(player)
    move = await client.request_move(possible_moves)
    move.apply(player, match)
    for player in match.players:
        if player.id != match.current_player:
            match.current_player = player.id
            break
    await matches.save(match)
    await match_channel.send('update')
