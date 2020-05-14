import asyncio

from gameplay.nano_magic.entities.player import Player
from gameplay.nano_magic.entities.match import Match

from gameplay.nano_magic.use_cases.messages import REQUEST_PLAY, set_hand, set_board


async def play_card(player: Player, match: Match):
    if match.players[1] == player:
        while True:
            await asyncio.sleep(1000)

    await player.channel.send(REQUEST_PLAY)
    card_index = await player.channel.receive()
    card_index = int(card_index)
    card = player.hand.pop(card_index)
    player.board.append(card)
    hand_message = set_hand(player.hand)
    await player.channel.send(hand_message)
    board_message = set_board()
    await player.channel.send(board_message)
    # await other_player.channel.send(board_message)



