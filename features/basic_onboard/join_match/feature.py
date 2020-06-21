from adapters.match_channel import MatchChannel
from entities.match import Match
from features.basic_onboard.join_match.clients import JoinMatchClient
from features.basic_onboard.join_match.repositories import JoinMatchRepository, MatchAlreadyReadyException


class JoinMatch:

    def __init__(self,
                 client: JoinMatchClient,
                 matches: JoinMatchRepository):
        self.match_client: MatchChannel = None
        self.client = client
        self.matches = matches

    async def execute(self, match: Match, player):
        try:
            match = await self.matches.join_and_get_if_still_waiting(match, player)
            if match.is_ready():
                match.yield_priority()
                await self.match_client.update()
        except MatchAlreadyReadyException as exception:
            await self.client.failed_to_join_match(match)
            raise exception
