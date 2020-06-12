from nano_magic.entities.match import Match
from nano_magic.repositories.match import MatchRepository


async def select_match(client, matches: MatchRepository, channel_factory):
    while True:
        match_id = await client.request_match_id()
        match_password = await client.request_match_password()
        match = await matches.get_by_id(match_id)
        if match:
            if match.check_password(match_password):
                return match
        else:
            channel = await channel_factory(match_id)
            match = Match(
                match_id,
                match_password,
                channel)
            await matches.save(match)
            return match
