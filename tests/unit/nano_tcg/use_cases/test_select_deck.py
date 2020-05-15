from unittest.mock import MagicMock

import pytest

from nano_magic.use_cases.select_deck import select_deck


@pytest.mark.asyncio
async def test_select_deck(deck_list, cards):
    class AsyncIterator:
        """
        https://stackoverflow.com/questions/36695256/python-asyncio-how-to-mock-aiter-method
        """

        def __init__(self, seq):
            self.iter = iter(seq)

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self.iter)
            except StopIteration:
                raise StopAsyncIteration

    client = MagicMock()
    client.request_deck.return_value = AsyncIterator(
        deck_list.split('\n')
    )
    deck = await select_deck(client)
    assert cards == deck
