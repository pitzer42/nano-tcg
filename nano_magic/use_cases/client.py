from abc import ABC
from typing import Iterable, List


class Client(ABC):

    async def request_player_id(self) -> str:
        raise NotImplementedError()

    async def request_deck(self) -> Iterable[str]:
        raise NotImplementedError()

    async def request_match_id(self) -> str:
        raise NotImplementedError()

    async def request_match_password(self) -> str:
        raise NotImplementedError()

    async def prompt_mulligan(self, hand: List[str]) -> bool:
        raise NotImplementedError()

    async def set_hand(self, hand: List[str]):
        raise NotImplementedError()

    async def request_card_in_hand(self) -> int:
        raise NotImplementedError()

    async def send_wait(self):
        raise NotImplementedError()

    async def set_board(self, board: List[str]):
        raise NotImplementedError()
