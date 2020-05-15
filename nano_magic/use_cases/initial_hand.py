from typing import List

from nano_magic.entities import draw
from nano_magic.entities.deck import shuffle
from nano_magic.use_cases.client import Client
from nano_magic.entities.player import Player

INITIAL_HAND_SIZE = 7


async def draw_initial_hand(client: Client, deck: List[str], hand_size=INITIAL_HAND_SIZE):
    if hand_size < 1:
        return []
    shuffle(deck)
    hand = list()
    draw(hand_size, deck, hand)
    mulligan = await client.prompt_mulligan(hand)
    if mulligan:
        draw(hand_size, hand, deck)
        return await draw_initial_hand(
            client,
            deck,
            hand_size - 1)
    return hand


async def set_hand(client: Client, player: Player, hand: List[str]):
    await client.set_hand(hand)
    player.hand = hand

