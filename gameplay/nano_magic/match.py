import asyncio

from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import Player, Match

PLAYERS_IN_MATCH = 2

matches = dict()


async def setup_match(player: Player):
    await request_match(player)
    await player.channel.send(protocol.WAITING_OTHER_PLAYERS)
    await player.match.is_ready()

    return

    await player.channel.send(protocol.START)

    player_index = player.match.index(player)

    # Hold player connection
    if player_index != 0:
        while True:
            await asyncio.sleep(1000)

    await player.channel.send(protocol.MAIN_PHASE)
    card_index = await player.channel.receive()
    card = player.hand.pop(card_index)
    player.board.append(card)
    await player.channel.send(protocol.UPDATE_HAND + ' ' + str(player.hand))
    await player.channel.send(protocol.UPDATE_BOARD + ' ' + str(player.board))


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