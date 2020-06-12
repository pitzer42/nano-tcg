from channels import Channel


class Observer:

    def __init__(self, channel: Channel, serialize):
        self.channel = channel
        self.serialize = serialize

    def notify(self, state):
        message = self.serialize(state)
        self.channel.send(message)

