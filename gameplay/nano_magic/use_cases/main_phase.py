from typing import List

from gameplay.nano_magic.entities import move
from gameplay.nano_magic.use_cases.client import Client


async def play_card(foo: Client, hand: List[str], board: List[str]):
    while True:
        card_index = await foo.request_card_in_hand()
        if card_index > -1:
            move(card_index, hand, board)
        else:
            return
