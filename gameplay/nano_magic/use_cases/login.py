from channels import Channel
from gameplay.nano_magic.entities.player import Player
from gameplay.nano_magic.use_cases.messages import REQUEST_PLAYER_ID

used_ids = set()


async def login(channel: Channel):
    player_id = await request_player_id(
        channel,
        lambda i: i not in used_ids
    )

    used_ids.add(player_id)

    return Player(
        channel,
        player_id
    )


async def request_player_id(channel: Channel, is_valid):
    while True:
        await channel.send(REQUEST_PLAYER_ID)
        player_id = await channel.receive()
        if is_valid(player_id):
            return player_id
