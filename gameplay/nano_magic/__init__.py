import asyncio

from channels import Channel
from gameplay.nano_magic.use_cases import messages
from gameplay.nano_magic.use_cases.initial_hand import draw_initial_hand
from gameplay.nano_magic.use_cases.login import login
from gameplay.nano_magic.use_cases.select_deck import select_deck
from gameplay.nano_magic.use_cases.select_match import select_match, join_match


async def play(channel: Channel):
    player = await login(channel)
    player.deck = await select_deck(channel)
    match = await select_match(channel)
    await join_match(player, match)
    await draw_initial_hand(player)

    while player_index == 1:
        await asyncio.sleep(1000)

    card_index = None
    while card_index != -1:
        card_index = await channel.send(messages.REQUEST_PLAY)
        card = initial_hand.pop(card_index)
        board = list()
        board.append(card)
        await channel.send(messages.set_board(board))

    attackers = await channel.send(messages.DECLARE_ATTACK)
