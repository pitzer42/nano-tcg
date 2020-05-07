from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import Player, Deck

from gameplay.nano_magic.deck_list import parse

lobby = dict()


async def setup_player(player: Player):
    await request_name(player)
    await request_deck(player)


async def request_name(player: Player):
    while True:
        await player.channel.send(protocol.REQUEST_NAME)
        user_name = await player.channel.receive()
        if user_name not in lobby:
            player.name = user_name
            lobby[user_name] = player
            break


async def request_deck(player: Player):
    while True:
        await player.channel.send(protocol.REQUEST_DECK)
        deck = await player.channel.receive()
        deck = parse(deck)
        player.deck += deck
        if protocol.END_DECK in deck:
            deck_size_ack = len(player.deck)
            await player.channel.send(deck_size_ack)
            return

