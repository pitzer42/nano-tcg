import pytest

from nano_magic.adapters import messages
from tests.integration.tcp.bot import READ_FLAG


@pytest.mark.skip
@pytest.mark.asyncio
async def test_full(tcp_bot_factory):
    client_a_name = test_full.__name__ + '_a'
    client_b_name = test_full.__name__ + '_b'

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
                client_b_name,
                READ_FLAG,
                *deck,
                messages.END_DECK,
                READ_FLAG,
                match,
                READ_FLAG,
                password,
                READ_FLAG
            )

            assert logs_a == logs_b
            assert logs_a == [
                messages.REQUEST_PLAYER_ID,
                messages.REQUEST_DECK,
                messages.REQUEST_MATCH,
                messages.REQUEST_MATCH_PASSWORD,
                messages.WAITING_OTHER_PLAYERS
            ]

            logs_a = await client_a.send(
                READ_FLAG
            )

            logs_b = await client_b.send(
                READ_FLAG
            )

            assert messages.PROMPT_MULLIGAN in logs_a[-1]
            assert messages.PROMPT_MULLIGAN in logs_b[-1]


@pytest.mark.skip
@pytest.mark.asyncio
async def test_retry_request_name(tcp_bot_factory):
    client_a_name = test_retry_request_name.__name__ + '_a'
    client_b_name = test_retry_request_name.__name__ + '_b'

    async with tcp_bot_factory() as client_a:
        async with tcp_bot_factory() as client_b:
            logs_a = await client_a.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG
            )

            assert logs_a == [
                messages.REQUEST_PLAYER_ID,
                messages.REQUEST_DECK
            ]

            logs_b = await client_b.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG,
                client_a_name,
                READ_FLAG,
                client_b_name,
                READ_FLAG
            )

            assert logs_b == [
                messages.REQUEST_PLAYER_ID,
                messages.REQUEST_PLAYER_ID,
                messages.REQUEST_PLAYER_ID,
                messages.REQUEST_DECK
            ]
