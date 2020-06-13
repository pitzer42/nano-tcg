from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.use_cases.client import Client


async def sync(client: Client, player: Player, match: Match):
    await client.sync(player, match)
