from nano_magic.storage.memory import MemoryMatchRepository
from nano_magic.use_cases.client import Client
from nano_magic.use_cases.initial_hand import draw_initial_hand
from nano_magic.use_cases.login import login
from nano_magic.use_cases.main_phase import play_card
from nano_magic.use_cases.select_deck import select_deck
from nano_magic.use_cases.select_match import select_match
from nano_magic.use_cases.waiting import join

players = dict()
matches = MemoryMatchRepository()


async def play(client: Client, channel_factory):
    player = await login(client, players)
    player.deck = await select_deck(client)
    match = await select_match(client, matches, channel_factory)
    player_index = await join(client, player, match)
    player.hand = await draw_initial_hand(client, player.deck)
    while True:
        await match.to_be_turn(player_index)
        await play_card(client, player.hand, match.board)
        await match.next_turn()
