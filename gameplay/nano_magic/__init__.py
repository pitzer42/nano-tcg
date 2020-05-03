import random
import asyncio

from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import (
    Player,
    Match
)

from gameplay.nano_magic.player_setup import setup_player
from gameplay.nano_magic.match_setup import setup_match


async def play(channel):
    player = Player(channel)
    await setup_player(player)
    await setup_match(player)
    await player.match.run()

    await handle_deck_shuffle(player)
    await handle_initial_draw(player)
    if len(player.hand) == 0:
        await player.channel.send('loser')

    # Start Sync Session

    current_player_index = random.randint(0, 1)
    other_player_index = 1 - current_player_index

    current_player = player.match._players[current_player_index]
    other_player = player.match._players[other_player_index]

    while current_player == player:
        current_player = player.match._players[current_player_index]
        other_player = player.match._players[other_player_index]

        await current_player.channel.send('your turn')

        while True:
            await asyncio.sleep(1000)

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
        await handle_top_i_hand(player, 0)
    await handle_initial_draw(player, n_mulligan)





async def handle_draw(player, n=1):
    for i in range(n):
        card = player.deck.pop()
        player.hand.append(card)


async def handle_top_i_hand(player, i):
    card = player.hand.pop(i)
    player.deck.append(card)
