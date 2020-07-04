from gloop.channels import TcpChannel

READ_FLAG = '$read'


class TcpBot(TcpChannel):

    def __init__(self, host, port):
        super(TcpBot, self).__init__(host, port)

    async def send(self, *messages):
        responses = list()
        for message in messages:
            if message == READ_FLAG:
                response = await super(TcpBot, self).receive()
                responses.append(response)
            else:
                await super(TcpBot, self).send(message)
        return responses
