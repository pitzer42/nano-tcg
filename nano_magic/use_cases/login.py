from nano_magic.entities.player import Player

from nano_magic.use_cases.client import Client


async def login(client: Client, players):
    player_id = await request_available_user_id(client, players)
    player = Player(player_id)
    players[player_id] = player
    return player


async def request_available_user_id(client: Client, players):
    while True:
        player_id = await client.request_player_id()
        if player_id not in players:
            return player_id
