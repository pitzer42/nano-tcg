from nano_magic.use_cases.client import Client

from nano_magic.entities.match import Match


async def select_match(client: Client, matches: dict):
    while True:
        match_id = await client.request_match_id()
        match_password = await client.request_match_password()
        match = matches.get(match_id)
        if match:
            if match.check_password(match_password):
                return match
        else:
            match = Match(
                match_id,
                match_password)
            matches[match_id] = match
            return match
