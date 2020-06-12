from channels import Channel


class UseCase:

    def __init__(self, client_channel: Channel, shared_channel: Channel):
        self._client_channel = client_channel
        self._shared_channel = shared_channel


class Sync(UseCase):

    def __init__(self, client_channel: Channel, shared_channel: Channel):
        super(Sync, self).__init__(client_channel, shared_channel)

    def execute(self):
        while True:
            message = self._shared_channel.receive()


