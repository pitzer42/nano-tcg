from typing import List

from nano_magic.entities import move
from nano_magic.use_cases.client import Client


async def play_card(client: Client, hand: List[str], board: List[str]):
    while True:
        await client.set_board(board)
        card_index = await client.request_card_in_hand(hand)
        card = hand[card_index]
        if card_index > -1:
            move(card_index, hand, board)
        else:
            return
