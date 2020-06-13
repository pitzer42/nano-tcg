from tictactoe.entities.match import Match
from tictactoe.repositories.match import MatchRepository
from tictactoe.use_cases.client import Client


async def select_match(client: Client, matches: MatchRepository, channel_factory) -> Match:
    while True:
        all_matches = await matches.all_waiting()
        selected_id, password = await client.choose_match(all_matches)
        selected_match = None
        for match in all_matches:
            if selected_id == match.id:
                selected_match = match
                break
        if selected_match is None:
            channel = await channel_factory(selected_id)
            await channel.connect()
            match = Match(
                selected_id,
                password,
                channel
            )
            await matches.save(match)
            return match
        elif selected_match.check_password(password):
            selected_match.channel = await channel_factory(selected_id)
            await selected_match.channel.connect()
            return selected_match
