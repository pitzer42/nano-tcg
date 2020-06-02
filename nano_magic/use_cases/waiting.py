from nano_magic.adapters.client_channel import Client
from nano_magic.entities.match import Match
from nano_magic.entities.player import Player


async def join(client: Client, player: Player, match: Match):
    player_index = match.join(player)
    await client.send_wait()
    await match.to_be_ready()
    return player_index
