from channels import Channel
from gameplay.nano_magic import protocol


async def request_deck(channel: Channel):
    await channel.send(protocol.REQUEST_DECK)
    deck = list()
    while True:
        deck_str = await channel.receive()
        cards = parse_deck_str(deck_str)
        deck += cards
        if cards[-1] == protocol.END_DECK:
            deck.pop()
            ack = len(deck)
            await channel.send(ack)
            return deck


def parse_deck_str(deck_str: str):
    cards = list()
    deck_str = deck_str.split('\n')
    for deck_entry in deck_str:
        deck_entry = deck_entry.strip().lower()
        if deck_entry == '':
            continue
        try:
            first_space_index = deck_entry.index(' ')
            quantity_str = deck_entry[:first_space_index]
            quantity_str.replace('x', '')
            quantity_str = quantity_str.strip()
            quantity = int(quantity_str)
            card = deck_entry[first_space_index + 1:]
            card = card.strip()
        except:
            quantity = 1
            card = deck_entry.strip()

        cards += [card] * quantity

    return cards
