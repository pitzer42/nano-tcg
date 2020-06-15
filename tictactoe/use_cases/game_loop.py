from features.indentify_client.feature import IdentifyClient
from features.join_match.feature import JoinMatch
from features.join_match.repositories import MatchAlreadyReadyException
from features.select_or_create_match.feature import SelectOrCreateMatch
from tictactoe.entities.match import Match
from tictactoe.entities.player import Player
from tictactoe.repositories.match import MatchRepository
from tictactoe.repositories.player import PlayerRepository
from tictactoe.use_cases.client import Client
from tictactoe.use_cases.game_over import game_over
from tictactoe.use_cases.play import play
from tictactoe.use_cases.priority import has_priority
from tictactoe.use_cases.sync import sync


async def game_loop(client: Client, matches: MatchRepository, players: PlayerRepository, channel_factory):
    identify_user = IdentifyClient(
        client,
        players
    )

    async def match_factory(match_id, password):
        channel = await channel_factory(match_id)
        await channel.connect()
        return Match(
            match_id,
            password,
            channel
        )

    select_or_create_match = SelectOrCreateMatch(
        client,
        matches,
        match_factory
    )

    join_match = JoinMatch(
        client,
        matches
    )

    client_id = await identify_user.execute()
    player = Player(client_id)

    match: Match = None
    match_channel = None
    while True:
        match = await select_or_create_match.execute()
        match_channel = match.channel
        try:
            await join_match.execute(match, player)
            break
        except MatchAlreadyReadyException:
            pass  # retry

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
