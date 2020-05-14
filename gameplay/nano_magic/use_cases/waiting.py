from gameplay.nano_magic.adapters.client_channel import Client
from gameplay.nano_magic.entities.match import Match
from gameplay.nano_magic.entities.player import Player


async def join(client: Client, player: Player, match: Match):
    match.join(player)
    await client.send_wait()
    await match.is_ready()
