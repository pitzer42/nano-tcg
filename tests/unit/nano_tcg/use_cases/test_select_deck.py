from tests.unit import AsyncGeneratorMock

from unittest.mock import MagicMock

import pytest

from nano_magic.use_cases.select_deck import select_deck


@pytest.mark.asyncio
async def test_select_deck(deck_list, cards):
    client = MagicMock()
    client.request_deck.return_value = AsyncGeneratorMock(
        deck_list.split('\n')
    )
    deck = await select_deck(client)
    assert cards == deck
