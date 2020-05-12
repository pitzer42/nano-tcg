from channels import Channel

from gameplay.nano_magic.entities.match import Match
from gameplay.nano_magic.entities.player import Player
from gameplay.nano_magic.use_cases.messages import REQUEST_MATCH, REQUEST_MATCH_PASSWORD, WAITING_OTHER_PLAYERS

matches = dict()


async def select_match(channel: Channel):
    match_id, match_password = await request_match(
        channel,
        lambda i: i not in matches,
        lambda i: matches[i].password,
    )
    if match_id in matches:
        return matches[match_id]
    else:
        match = Match(match_id, match_password)
        matches[match_id] = match
        return match


async def request_match(player: Channel, is_unique, get_password):
    while True:
        await player.send(REQUEST_MATCH)
        id = await player.receive()
        await player.send(REQUEST_MATCH_PASSWORD)
        password = await player.receive()
        if is_unique(id):
            return id, password
        else:
            right_password = get_password(id)
            if right_password == password:
                return id, password


async def join_match(player: Player, match: Match):
    match.join(player)
    await player.send(WAITING_OTHER_PLAYERS)
    await match.is_ready()
