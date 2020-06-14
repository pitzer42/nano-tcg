from features.create_match.feature import CreateMatch
from features.indentify_client.feature import IdentifyClient
from features.select_match.feature import SelectMatch
from features.select_or_create_match.feature import SelectOrCreateMatch
from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.client import Client
from tictactoe.use_cases.game_over import game_over
from tictactoe.use_cases.join import join
from tictactoe.use_cases.play import play
from tictactoe.use_cases.priority import has_priority
from tictactoe.use_cases.sync import sync


async def game_loop(client: Client, matches: MatchRepository, players: PlayerRepository, channel_factory):
    identify_user = IdentifyClient(
        client,
        players
    )

    select_match = SelectMatch(
        client,
        matches
    )

    async def match_factory(match_id, password):
        channel = await channel_factory(match_id)
        await channel.connect()
        return Match(
            match_id,
            password,
            channel
        )

    create_match = CreateMatch(
        client,
        matches,
        match_factory
    )

    select_or_create_match = SelectOrCreateMatch(
        client,
        select_match,
        create_match
    )

    client_id = await identify_user.execute()
    player = Player(client_id)

    joined = False
    while not joined:
        match = await select_or_create_match.execute()
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
