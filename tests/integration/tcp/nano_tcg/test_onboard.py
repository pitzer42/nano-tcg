import pytest

from functools import partial

import server
import asyncio

from multiprocessing import Process

from modes.nano_magic import protocol

from tests.integration.tcp.bot import READ_FLAG, TcpBot


@pytest.mark.asyncio
async def test_full(tcp_bot_factory):

    client_a_name = test_full.__name__ + '_a'
    client_b_name = test_full.__name__ + '_b'
    deck = ['Storm Crow', 'Island'] * 4
    match = 'm1'
    password = '123'

    async with tcp_bot_factory() as client_a:
        async with tcp_bot_factory() as client_b:

            logs_a = await client_a.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG,
                *deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                match,
                READ_FLAG,
                password,
                READ_FLAG,
            )

            logs_b = await client_b.send(
                READ_FLAG,
                client_b_name,
                READ_FLAG,
                *deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                match,
                READ_FLAG,
                password,
                READ_FLAG,
            )

            assert logs_a == logs_b
            assert logs_a == [
                protocol.REQUEST_NAME,
                protocol.REQUEST_DECK,
                str(len(deck)),
                protocol.REQUEST_MATCH,
                protocol.REQUEST_MATCH_PASSWORD,
                protocol.WAITING_OTHER_PLAYERS
            ]

            # Read hands

            await client_a.send(
                READ_FLAG,
            )

            await client_b.send(
                READ_FLAG,
            )

            # Back to common test steps

            logs_a = await client_a.send(
                READ_FLAG,
                ''
            )

            logs_b = await client_b.send(
                READ_FLAG,
                ''
            )

            assert logs_a == logs_b
            assert logs_a == [
                protocol.PROMPT_MULLIGAN
            ]


@pytest.mark.asyncio
async def test_retry_request_name(tcp_bot_factory):

    client_a_name = test_full.__name__ + '_a'
    client_b_name = test_full.__name__ + '_b'

    async with tcp_bot_factory() as client_a:
        async with tcp_bot_factory() as client_b:

            logs_a = await client_a.send(
                READ_FLAG,
                client_a_name,
                READ_FLAG
            )

            assert logs_a == [
                protocol.REQUEST_NAME,
                protocol.REQUEST_DECK
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
                protocol.REQUEST_NAME,
                protocol.REQUEST_NAME,
                protocol.REQUEST_NAME,
                protocol.REQUEST_DECK
            ]