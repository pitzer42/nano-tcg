import sys
import asyncio

from gameplay import nano_magic

from channels.aio_stream import AioStreamChannel


async def start(port, accept):
    async def accept_streams(reader, writer):
        await accept(
            AioStreamChannel(
                reader,
                writer
            )
        )

    server = await asyncio.start_server(
        accept_streams,
        '127.0.0.1',
        port
    )
    async with server:
        await server.serve_forever()


def main(port=8888, accept=nano_magic.play):
    asyncio.run(
        start(
            port,
            accept
        )
    )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        main(port)
    else:
        main()
