from channels.tcp import TcpChannel

READ_FLAG = '$read'


class TestBot(TcpChannel):

    def __init__(self, host, port):
        super(TestBot, self).__init__(host, port)

    async def send(self, *messages):
        responses = list()
        for message in messages:
            if message == READ_FLAG:
                response = await super(TestBot, self).receive()
                responses.append(response)
            else:
                await super(TestBot, self).send(message)
        return responses
