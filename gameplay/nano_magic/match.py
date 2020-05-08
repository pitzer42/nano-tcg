from random import shuffle

from channels import Channel
from gameplay.nano_magic import protocol

PLAYERS_IN_MATCH = 2
INITIAL_HAND_SIZE = 7

matches = dict()


async def request_match(player: Channel, is_unique, get_password):
    while True:
        await player.send(protocol.REQUEST_MATCH)
        id = await player.receive()
        await player.send(protocol.REQUEST_MATCH_PASSWORD)
        password = await player.receive()
        if is_unique(id):
            return id, password
        else:
            right_password = get_password(id)
            if right_password == password:
                return id, password


async def draw_initial_hand(player: Channel, deck, hand_size=INITIAL_HAND_SIZE):
    shuffle(deck)
    hand = list()
    draw(hand_size, deck, hand)
    mulligan = await prompt_mulligan(player, hand)
    if hand_size > 1 and mulligan:
        draw(hand_size, hand, deck)
        return await draw_initial_hand(player, deck, hand_size - 1)
    return hand


def draw(n, deck, hand):
    drawn = deck[-n:]
    del deck[-n:]
    hand += drawn


async def prompt_mulligan(channel, hand):
    message = protocol.prompt_mulligan(hand)
    await channel.send(message)
    response = await channel.receive()
    return protocol.is_positive(response)
