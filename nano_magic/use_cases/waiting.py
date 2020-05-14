from nano_magic.adapters import Client
from nano_magic.entities import Match
from nano_magic.entities import Player


async def join(client: Client, player: Player, match: Match):
    match.join(player)
    await client.send_wait()
    await match.to_be_ready()
