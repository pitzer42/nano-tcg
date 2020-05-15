from nano_magic.use_cases.client import Client
from nano_magic.use_cases.initial_hand import draw_initial_hand
from nano_magic.use_cases.login import login
from nano_magic.use_cases.main_phase import play_card
from nano_magic.use_cases.select_deck import select_deck
from nano_magic.use_cases.select_match import select_match
from nano_magic.use_cases.waiting import join

players = dict()
matches = dict()


async def play(client: Client):
    player = await login(client, players)
    player.deck = await select_deck(client)
    match = await select_match(client, matches)
    await join(client, player, match)
    player.hand = await draw_initial_hand(client, player.deck)
    board = list()
    await play_card(client, player.hand, board)
