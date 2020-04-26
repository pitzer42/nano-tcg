import sys
import asyncio
import protocol


async def start_chat(users):
    n = len(users)
    while True:
        for i in range(n):
            i_user, i_pair = users[i]
            i_reader, i_writer = i_pair
            msg = await i_reader.readline()
            for j in range(i, n):
                j_user, j_pair = users[j]
                j_reader, j_writer = j_pair
                j_writer.write(msg)
                await j_writer.drain()


lobby = dict()


async def get_user_name(reader, writer):
    request_name_message = protocol.wrap_message(protocol.REQUEST_NAME)
    while True:
        writer.write(request_name_message)
        await writer.drain()
        user_name = await reader.readline()
        user_name = user_name.decode().strip()
        if user_name not in lobby:
            return user_name


async def handler(reader, writer):
    user_name = await get_user_name(reader, writer)
    lobby[user_name] = (reader, writer)
    while len(lobby.keys()) > 1:
        users = list(lobby.items())
        chat = users[:2]
        for user in chat:
            user_key = user[0]
            del lobby[user_key]
        # TODO: blocking?
        await start_chat(chat)


async def start(port=8888):
    server = await asyncio.start_server(
        handler,
        '127.0.0.1',
        port
    )
    async with server:
        await server.serve_forever()


def main(_port=8888):
    asyncio.run(
        start(
            port=_port
        )
    )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _port = int(sys.argv[1])
        main_coroutine = start(
            port=_port
        )
    else:
        main_coroutine = start()
    asyncio.run(main_coroutine)
