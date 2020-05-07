from gameplay.nano_magic import protocol
from gameplay.nano_magic.models import (
    Player,
    Match
)

from gameplay.nano_magic.player_setup import setup_player
from gameplay.nano_magic.match_setup import setup_match


async def play(channel):
    player = Player(channel)
    await setup_player(player)
    await setup_match(player)
    await player.match.run(player)
