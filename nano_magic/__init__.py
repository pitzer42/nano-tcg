from nano_magic.use_cases.client import Client
from nano_magic.use_cases import draw_initial_hand
from nano_magic.use_cases import login
from nano_magic.use_cases import play_card
from nano_magic.use_cases import select_deck
from nano_magic.use_cases import select_match
from nano_magic.use_cases import join

players = dict()
matches = dict()


async def play(client: Client):
    player = await login(client, players)
    player.deck = await select_deck(client)
    match = await select_match(client, matches)
    await join(client, player, match)
    player.hand = await draw_initial_hand(client, player.deck)
    await play_card(player, match)
