import random
import asyncio

from modes.nano_magic import protocol
from modes.nano_magic.models import (
    Player,
    Match
)

lobby = dict()
matches = dict()


async def accept(channel):
    player = Player()
    player.channel = channel

    player.name = await handle_get_user_name(player.channel)
    lobby[player.name] = player

    player.deck = await handle_request_deck(player.channel)
    deck_size_ack = str(len(player.deck))
    await player.channel.send(deck_size_ack)

    match = await handle_request_match(player.channel)
    match.players.append(player)

    await player.channel.send(protocol.WAITING_OTHER_PLAYERS)

    while len(match.players) < 2:
        await asyncio.sleep(1)

    await player.channel.send('start!')

    await handle_deck_shuffle(player)
    await handle_initial_draw(player)
    if len(player.hand) == 0:
        await player.channel.send('loser')

    # while True:
      #  await asyncio.sleep(100)

    current_player_index = random.randint(0, 1)
    other_player_index = 1 - current_player_index

    while not await game_over(match):
        current_player = match.players[current_player_index]
        other_player = match.players[other_player_index]

        await current_player.channel.send('your turn')

        await upkeep(current_player)
        await handle_draw(current_player)
        await main_phase(current_player)
        await begining_combat(current_player)
        await declare_attackers(current_player)
        await declare_blockers(other_player)
        await combat(other_player)
        await main_phase(current_player)
        await end_step(current_player)
        current_player_index = 1 - current_player_index
        other_player_index = 1 - other_player_index


async def game_over(match):
    return False


async def upkeep(player):
    pass


async def main_phase(player):
    pass


async def begining_combat(player):
    pass


async def declare_attackers(player):
    pass


async def declare_blockers(player):
    pass


async def combat(player):
    pass


async def end_step(player):
    pass


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
