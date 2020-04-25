import asyncio


async def handler(reader, writer):
    while True:
        line = await reader.readline()
        writer.write(line)
        await writer.drain()


async def main():
    server = await asyncio.start_server(
        handler,
        '127.0.0.1',
        8888
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
