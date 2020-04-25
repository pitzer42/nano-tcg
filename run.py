import sys
import asyncio


async def handler(reader, writer):
    while True:
        line = await reader.readline()
        writer.write(line)
        await writer.drain()


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
