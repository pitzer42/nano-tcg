from typing import List

from gameplay.nano_magic.entities import draw
from gameplay.nano_magic.entities.deck import shuffle
from gameplay.nano_magic.use_cases.client import Client

INITIAL_HAND_SIZE = 7


async def draw_initial_hand(client: Client, deck: List[str], hand_size=INITIAL_HAND_SIZE):
    if hand_size < 1:
        return
    shuffle(deck)
    hand = list()
    draw(hand_size, deck, hand)
    mulligan = await client.prompt_mulligan(hand)
    if mulligan:
        draw(hand_size, hand, deck)
        return await draw_initial_hand(
            deck,
            client,
            hand_size - 1)
    return hand
