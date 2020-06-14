from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.client import Client
from tictactoe.use_cases.game_over import game_over
from tictactoe.use_cases.join import join
from tictactoe.use_cases.login import login
from tictactoe.use_cases.play import play
from tictactoe.use_cases.priority import has_priority
from tictactoe.use_cases.select_match import select_match
from tictactoe.use_cases.sync import sync


async def game_loop(client: Client, matches: MatchRepository, players: PlayerRepository, channel_factory):
    player = await login(client, players)

    joined = False
    while not joined:
        match = await select_match(client, matches, channel_factory)
        match_channel = match.channel
        joined = await join(player, match, matches)
        if not joined:
            await client.failed_to_join_match(match)
        match = joined

    _game_over = False
    while not _game_over:
        await sync(client, player, match)
        if await has_priority(client, player, match, matches, match_channel):
            await sync(client, player, match)
            _game_over = await game_over(match, matches, client, player)
            if _game_over:
                break

            await play(client, player, match, match_channel, matches)

            await sync(client, player, match)
            _game_over = await game_over(match, matches, client, player)
            if _game_over:
                break
