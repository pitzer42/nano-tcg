from gameplay.nano_magic.entities.deck import deck_parser

from gameplay.nano_magic.use_cases.client import Client


async def select_deck(client: Client):
    deck = list()
    async for deck_entry in client.request_deck():
        cards = deck_parser(deck_entry)
        deck += cards
    return deck
