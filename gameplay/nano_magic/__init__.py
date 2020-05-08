import asyncio

from channels import Channel
from gameplay.nano_magic import protocol

from gameplay.nano_magic.login import request_name
from gameplay.nano_magic.deck import request_deck
from gameplay.nano_magic.match import request_match
from gameplay.nano_magic.match import draw_initial_hand

lobby = dict()
matches = dict()


async def play(channel: Channel):
    user_name = await request_name(
        channel,
        lambda i: i not in lobby
    )
    lobby[user_name] = channel

    deck = await request_deck(channel)

    match_id, match_password = await request_match(
        channel,
        lambda i: i not in matches,
        matches.__getitem__,
    )
    matches[match_id] = match_password

    await channel.send(protocol.WAITING_OTHER_PLAYERS)

    initial_hand = await draw_initial_hand(channel, deck)

    await asyncio.sleep(1000)
