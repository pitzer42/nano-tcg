from tictactoe.entities.player import Player
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.client import Client


async def login(client: Client, players: PlayerRepository):
    while True:
        player_id = await client.request_player_id()
        player = await players.get_by_id(player_id)
        if not player:
            player = Player(player_id)
            await players.save(player)
            return player
