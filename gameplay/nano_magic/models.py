import asyncio
import random
import json

from gameplay.nano_magic import protocol
from gameplay.nano_magic.deck_list import parse


class Card:

    def __init__(self):
        self.name = 'Card 1'


class Player:

    def __init__(self, channel):
        self.channel = channel
        self.name = ''
        self.hand = list()
        self.board = list()
        self.deck = Deck()
        self.match = None

    def draw(self, n=1):
        for i in range(n):
            card = self.deck.pop()
            self.hand.append(card)

    def shuffle_hand_into_deck(self):
        self.deck += self.hand
        self.hand.clear()
        self.deck.shuffle()


class Match:
    REQUIRED_PLAYER_QUANTITY = 2
    INITIAL_HAND_SIZE = 7

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self._players = list()
        self._is_ready = asyncio.Event()

    async def is_ready(self):
        await self._is_ready.wait()

    def add_player(self, player: Player):
        player_quantity = len(self._players)
        if player_quantity == Match.REQUIRED_PLAYER_QUANTITY:
            message = f'match {self.name} already has {Match.REQUIRED_PLAYER_QUANTITY} players.'
            raise Exception(message)
        player.match = self
        self._players.append(player)
        if player_quantity + 1 == Match.REQUIRED_PLAYER_QUANTITY:
            self._is_ready.set()

    async def run(self, player: Player):
        player.deck.shuffle()
        await self.draw_initial_hand(player)
        # self._players.sort() TypeError: '<' not supported between instances of 'Player' and 'Player'
        player_index = self._players.index(player)

        # keep all players alive
        if player_index != 0:
            while True:
                await asyncio.sleep(1000)


    async def draw_initial_hand(self, player: Player):
        hand_size = Match.INITIAL_HAND_SIZE
        player.draw(hand_size)
        message = protocol.PROMPT_MULLIGAN + ' ' +json.dumps(player.hand)
        await player.channel.send(message)
        mulligan = await player.channel.receive()
        while mulligan and hand_size > 0:
            player.shuffle_hand_into_deck()
            hand_size -= 1
            player.draw(hand_size)
            message = protocol.PROMPT_MULLIGAN + ' ' + json.dumps(player.hand)
            await player.channel.send(message)
            mulligan = await player.channel.receive()


class Deck(list):

    @staticmethod
    def from_deck_list(deck_list: str):
        lines = deck_list.split('\n')
        deck = Deck()
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            try:
                first_space_index = line.index(' ')
                quantity = int(line[:first_space_index])
                card = line[first_space_index + 1:]
                deck += [card] * quantity
            except ValueError:
                # line does not contain quantity
                deck.append(line)
        return deck

    def shuffle(self):
        random.seed(id(self))
        random.shuffle(self)
