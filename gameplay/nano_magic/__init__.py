import asyncio

from channels import Channel
from gameplay.nano_magic.use_cases import messages
from gameplay.nano_magic.use_cases.initial_hand import draw_initial_hand
from gameplay.nano_magic.use_cases.login import login
from gameplay.nano_magic.use_cases.select_deck import select_deck
from gameplay.nano_magic.use_cases.select_match import select_match, join_match
from gameplay.nano_magic.use_cases.main_phase import play_card



async def play(channel: Channel):
    player = await login(channel)
    player.deck = await select_deck(channel)
    match = await select_match(channel)
    await join_match(player, match)
    player.hand = await draw_initial_hand(player)
    await play_card(player, match)
