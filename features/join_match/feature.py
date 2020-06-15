from entities.match import Match
from features.join_match.client import JoinMatchClient
from features.join_match.repositories import JoinMatchRepository, MatchAlreadyReadyException


class JoinMatch:

    def __init__(self,
                 client: JoinMatchClient,
                 matches: JoinMatchRepository):
        self.client = client
        self.matches = matches

    async def execute(self, match: Match, player):
        try:
            match = await self.matches.join_and_get_if_still_waiting(match, player)
            if match.is_ready():
                await match.notify_is_ready()
        except MatchAlreadyReadyException as exception:
            await self.client.failed_to_join_match(match)
            raise exception
