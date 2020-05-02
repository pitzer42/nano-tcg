class Player:

    def __init__(self):
        self.channel = None
        self.name = ''
        self.hand = list()
        self.deck = list()


class Match:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.players = list()
