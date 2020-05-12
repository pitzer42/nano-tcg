from channels import Channel
from gameplay.nano_magic.entities.deck import deck_parser
from gameplay.nano_magic.use_cases.messages import REQUEST_DECK, END_DECK


async def select_deck(channel: Channel):
    await channel.send(REQUEST_DECK)
    deck = list()
    while True:
        deck_str = await channel.receive()
        cards = deck_parser(deck_str)
        deck += cards
        if len(cards) > 0 and cards[-1] == END_DECK:
            deck.pop()
            ack = len(deck)
            await channel.send(ack)
            return deck
