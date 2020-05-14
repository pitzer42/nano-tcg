from gameplay.nano_magic.adapters import messages
from gameplay.nano_magic.use_cases.client import Client
from gameplay.nano_magic.use_cases.initial_hand import draw_initial_hand
from gameplay.nano_magic.use_cases.login import login
from gameplay.nano_magic.use_cases.main_phase import play_card
from gameplay.nano_magic.use_cases.select_deck import select_deck
from gameplay.nano_magic.use_cases.select_match import select_match
from gameplay.nano_magic.use_cases.waiting import join

players = dict()
matches = dict()


async def play(client: Client):
    player = await login(client, players)
    player.deck = await select_deck(client)
    match = await select_match(client, matches)
    await join(client, player, match)
    player.hand = await draw_initial_hand(client, player.deck)
    await play_card(player, match)
