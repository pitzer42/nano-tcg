from channels import Channel


class Match:

    def __init__(self, match_id, password, channel: Channel):
        self.id = match_id
        self.players = list()
        self.channel = channel
        self.check_password = lambda a: a == password
