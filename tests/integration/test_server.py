import pytest
import asyncio

from functools import partial
from multiprocessing import Process

import server
from modes.nano_magic import protocol

from bot import TestBot, READ_FLAG


@pytest.fixture
async def running_server(unused_tcp_port):
    if False:
        yield '127.0.0.1', 8888
        return

    host = '127.0.0.1'
    port = unused_tcp_port
    delay = 1

    start_test_server = partial(
        server.main,
        port
    )

    server_process = Process(
        target=start_test_server
    )
    server_process.start()

    await asyncio.sleep(delay)
    yield host, port

    server_process.kill()


@pytest.fixture
def bot_factory(running_server):
    host, port = running_server
    return partial(TestBot, host, port)


@pytest.mark.asyncio
async def test_invalid_user_name(bot_factory):
    async with bot_factory() as client_1:
        client_1_log = await client_1.send(
            READ_FLAG,
            'test_invalid_user_name_a'
        )

    async with bot_factory() as client_2:
        client_2_log = await client_2.send(
            READ_FLAG,
            'test_invalid_user_name_a',
            READ_FLAG,
            'test_invalid_user_name_a',
            READ_FLAG,
            'test_invalid_user_name_b'
        )

    assert client_1_log == [protocol.REQUEST_NAME] * 1
    assert client_2_log == [protocol.REQUEST_NAME] * 3


@pytest.mark.asyncio
async def test_deck_request(bot_factory):
    async with bot_factory() as a:
        logs = await a.send(
            READ_FLAG,
            'test_deck_request',
            READ_FLAG,
            '4 Serra Angel',
            '20 Plain',
            protocol.END_DECK,
            READ_FLAG
        )

    assert logs == [
        protocol.REQUEST_NAME,
        protocol.REQUEST_DECK,
        '2'
    ]


@pytest.mark.asyncio
async def test_request_match(bot_factory):

    async with bot_factory() as a:
        async with bot_factory() as b:

            log_a = await a.send(
                READ_FLAG,
                'test_request_match_a',
                READ_FLAG,
                'serra angel',
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            log_b = await b.send(
                READ_FLAG,
                'test_request_match_b',
                READ_FLAG,
                'slippery bogle',
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            assert protocol.WAITING_OTHER_PLAYERS in log_a
            assert protocol.WAITING_OTHER_PLAYERS in log_b


@pytest.mark.asyncio
async def test_request_mulligan(bot_factory):

    async with bot_factory() as a:
        async with bot_factory() as b:

            deck = ['serra angel'] * 60
            fa = await a.send(
                READ_FLAG,
                'test_request_match_a',
                READ_FLAG,
                * deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            await b.send(
                READ_FLAG,
                'test_request_match_b',
                READ_FLAG,
                * deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            log_a = await a.send(
                READ_FLAG,
                READ_FLAG,
                READ_FLAG,
                ''
            )

            log_b = await b.send(
                READ_FLAG,
                READ_FLAG,
                READ_FLAG,
                ''
            )

            assert protocol.PROMPT_MULLIGAN in log_a
            assert protocol.PROMPT_MULLIGAN in log_b


@pytest.mark.asyncio
async def test_request_main(bot_factory):

    deck = ['serra angel'] * 60

    async with bot_factory() as a:
        async with bot_factory() as b:
            log_a = await a.send(
                READ_FLAG,
                'test_request_match_a',
                READ_FLAG,
                *deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            log_b = await b.send(
                READ_FLAG,
                'test_request_match_b',
                READ_FLAG,
                *deck,
                protocol.END_DECK,
                READ_FLAG,
                READ_FLAG,
                'match1',
                READ_FLAG,
                '123',
                READ_FLAG
            )

            """
            start!
            hand array
            mulligan?
            send something
            firt?
            """

            log_a += await a.send(
                READ_FLAG,
                READ_FLAG,
                READ_FLAG,
                ''
            )

            log_b += await b.send(
                READ_FLAG,
                READ_FLAG,
                READ_FLAG,
                '',
                READ_FLAG
            )

            log_a += await a.send(
                READ_FLAG
            )

            log_b += await b.send(
                READ_FLAG
            )

            print('=============================log_a')
            print(log_a)
            print('=============================log_b')
            print(log_b)
