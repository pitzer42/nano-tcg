from channels import Channel

from gameplay.nano_magic import protocol


async def request_name(channel: Channel, is_valid):
    while True:
        await channel.send(protocol.REQUEST_NAME)
        user_name = await channel.receive()
        if is_valid(user_name):
            return user_name
