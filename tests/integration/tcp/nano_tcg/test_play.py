import pytest

from nano_magic.adapters import messages
from tests.integration.tcp.bot import READ_FLAG


@pytest.mark.skip
@pytest.mark.asyncio
async def test_play_card(tcp_bot_factory):
    client_a_name = test_play_card.__name__ + '_a'
    client_b_name = test_play_card.__name__ + '_b'

    deck = ['4 Storm Crow', '4 Island']
    expected_deck_length = '8'
    match = 'm1'
    password = '123'

    async with tcp_bot_factory() as client_a:
        async with tcp_bot_factory() as client_b:
            logs_a = await client_a.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG,
                *deck,
                messages.END_DECK,
                READ_FLAG,
                match,
                READ_FLAG,
                password,
                READ_FLAG
            )

            logs_b = await client_b.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG,
                *deck,
                messages.END_DECK,
                READ_FLAG,
                match,
                READ_FLAG,
                password,
                READ_FLAG
            )

            logs_a = await client_a.send(
                READ_FLAG,
                'n'
            )

            logs_b = await client_b.send(
                READ_FLAG,
                'n'
            )

            logs_a = await client_a.send(
                READ_FLAG,
                READ_FLAG,
                '0',
                '-1'
            )

            assert messages.SET_BOARD in logs_a[0]
            assert messages.REQUEST_PLAY in logs_a[1]
