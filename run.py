import sys
import asyncio


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


async def handler(reader, writer):
    INVALID_USER_NAME_MSG = b'invalid user name. Please, try again.\n'
    user_name = await reader.readline()
    user_name = user_name.decode().strip()
    while user_name in lobby:
        writer.write(INVALID_USER_NAME_MSG)
        await writer.drain()
        user_name = await reader.readline()
        user_name = user_name.decode().strip()
    lobby[user_name] = (reader, writer)
    while len(lobby.keys()) > 1:
        users = list(lobby.items())
        chat = users[:2]
        for user in chat:
            user_key = user[0]
            del lobby[user_key]
        # TODO: blocking?
        await start_chat(chat)




async def start_server(port):
    server = await asyncio.start_server(
        handler,
        '127.0.0.1',
        port
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    asyncio.run(start_server(port))
