from typing import Iterable, List

from channels import Channel
from nano_magic.adapters import messages
from nano_magic.use_cases.client import Client


class ClientChannel(Client):

    def __init__(self, channel: Channel):
        self._channel = channel

    async def request_player_id(self) -> str:
        await self._channel.send(messages.REQUEST_PLAYER_ID)
        return await self._channel.receive()

    async def request_deck(self) -> Iterable[str]:
        await self._channel.send(messages.REQUEST_DECK)
        while True:
            deck_entry = await self._channel.receive()
            if deck_entry == messages.END_DECK:
                return
            yield deck_entry

    async def request_match_id(self) -> str:
        await self._channel.send(messages.REQUEST_MATCH)
        return await self._channel.receive()

    async def request_match_password(self) -> str:
        await self._channel.send(messages.REQUEST_MATCH_PASSWORD)
        return await self._channel.receive()

    async def prompt_mulligan(self, hand) -> bool:
        message = messages.prompt_mulligan(hand)
        await self._channel.send(message)
        mulligan = await self._channel.receive()
        return mulligan in messages.POSITIVES

    async def request_card_in_hand(self, cards) -> int:
        while True:
            message = messages.request_play(cards)
            await self._channel.send(message)
            card_i = await self._channel.receive()
            try:
                return int(card_i)
            except ValueError:
                pass

    async def set_hand(self, hand: List[str]):
        message = messages.set_hand(hand)
        await self._channel.send(message)

    async def send_wait(self):
        await self._channel.send(messages.WAITING_OTHER_PLAYERS)

    async def set_board(self, board: List[str]):
        message = messages.set_board(board)
        await self._channel.send(message)


