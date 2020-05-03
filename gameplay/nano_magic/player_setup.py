from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import Player, Deck

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
    await player.channel.send(protocol.REQUEST_DECK)
    lines = list()
    while True:
        line = await player.channel.receive()
        if line == protocol.END_DECK:
            break
        lines.append(line)
    deck_list = '\n'.join(lines)
    player.deck = Deck.from_deck_list(deck_list)
    deck_size_ack = str(len(player.deck))
    await player.channel.send(deck_size_ack)
