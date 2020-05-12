from gameplay.nano_magic.entities import draw
from gameplay.nano_magic.entities.deck import shuffle
from gameplay.nano_magic.entities.player import Player
from gameplay.nano_magic.use_cases.messages import is_positive
from gameplay.nano_magic.use_cases.messages import set_hand
from gameplay.nano_magic.use_cases.messages import prompt_mulligan

INITIAL_HAND_SIZE = 7


async def initial_hand(player: Player):
    player.hand = await draw_initial_hand(player)
    await set_hand(player)


async def draw_initial_hand(player: Player, hand_size=INITIAL_HAND_SIZE):
    hand = list()
    if hand_size > 0:
        shuffle(player.deck)
        draw(hand_size, player.deck, hand)
        if hand_size > 1:
            mulligan = await _prompt_mulligan(player, hand)
            if mulligan:
                # place hand into deck
                draw(hand_size, hand, player.deck)
                return await draw_initial_hand(
                    player,
                    hand_size - 1)
    return hand


async def set_hand(player):
    message = set_hand(player.hand)
    await player.send(message)


async def _prompt_mulligan(channel, hand):
    message = prompt_mulligan(hand)
    await channel.send(message)
    response = await channel.receive()
    return is_positive(response)
