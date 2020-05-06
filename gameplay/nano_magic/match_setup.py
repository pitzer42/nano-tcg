import asyncio

from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import Player, Match

PLAYERS_IN_MATCH = 2

matches = dict()


async def setup_match(player: Player):
    await request_match(player)
    await player.channel.send(protocol.WAITING_OTHER_PLAYERS)
    await player.match.is_ready()

    print(player.match.name + ' ready')


async def request_match(player: Player):
    while True:
        await player.channel.send(protocol.REQUEST_MATCH)
        match_id = await player.channel.receive()
        await player.channel.send(protocol.REQUEST_MATCH_PASSWORD)
        password = await player.channel.receive()
        if match_id not in matches:
            match = Match(match_id, password)
            matches[match_id] = match
            break
        else:
            match = matches[match_id]
            if match.password == password:
                break
    match.add_player(player)
