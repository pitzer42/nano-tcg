import random

from channels import TcpChannel
from modes.nano_magic import protocol
from modes.nano_magic.models import (
    Player,
    Match
)


lobby = dict()
matches = dict()


async def accept(reader, writer):
    player = Player()
    player.channel = TcpChannel.from_stream(
        reader,
        writer
    )

    player.name = await handle_get_user_name(player.channel)
    lobby[player.name] = player

    player.deck = await handle_request_deck(player.channel)
    deck_size_ack = str(len(player.deck))
    await player.channel.send(deck_size_ack)

    match = await handle_request_match(player.channel)
    match.players.append(player)

    await player.channel.send('waiting for other player...')

    if len(match.players) == 2:
        for player in match.players:
            await player.channel.send('start!')
            await handle_deck_shuffle(player)
            await handle_initial_draw(player)
            if len(player.hand) == 0:
                await player.channel.send('loser')



async def handle_get_user_name(channel):
    while True:
        await channel.send(protocol.REQUEST_NAME)
        user_name = await channel.receive()
        if user_name not in lobby:
            return user_name


async def handle_request_deck(channel):
    await channel.send(protocol.REQUEST_DECK)
    deck_file_lines = list()
    while True:
        line = await channel.receive()
        if line == protocol.END_DECK:
            break
        deck_file_lines.append(line)
    return deck_file_lines


async def handle_request_match(channel):
    while True:
        await channel.send(protocol.REQUEST_MATCH)
        match_id = await channel.receive()
        await channel.send(protocol.REQUEST_MATCH_PASSWORD)
        password = await channel.receive()
        if match_id not in matches:
            match = Match(match_id, password)
            matches[match_id] = match
            return match
        else:
            match = matches[match_id]
            if match.password == password:
                return match


async def handle_initial_draw(player, n_mulligan=0):
    size = 7 - n_mulligan
    if size <= 0:
        return
    await handle_draw(player, n=size)
    await player.channel.send(str(player.hand))
    await player.channel.send(protocol.PROMPT_MULLIGAN)
    mulligan = await player.channel.receive()
    if mulligan:
        await handle_mulligan(
            player,
            n_mulligan=n_mulligan + 1
        )


async def handle_mulligan(player, n_mulligan):
    for i in range(len(player.hand)):
        await handle_top_i_hand(player, i)
    await handle_deck_shuffle(player)
    await handle_initial_draw(player, n_mulligan)


async def handle_deck_shuffle(player):
    random.seed(player.name + str(lobby))
    random.shuffle(player.deck)


async def handle_draw(player, n=1):
    for i in range(n):
        card = player.deck.pop()
        player.hand.append(card)


async def handle_top_i_hand(player, i):
    card = player.hand.pop(i)
    player.deck.append(card)
