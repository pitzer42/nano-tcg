from entities.player import Player
from features.identify_client.feature import IdentifyClient
from features.basic_onboard.join_match.feature import JoinMatch
from features.basic_onboard.join_match.repositories import MatchAlreadyReadyException
from features.basic_onboard.select_or_create_match.feature import SelectOrCreateMatch


class BasicOnboard:

    def __init__(self,
                 login):
        self.login = login

    async def execute(self):
        player = await self.login.execute()

        while True:
            match, match_client = await self.select_or_create_match.execute()
            self.join_match.match_client = match_client
            try:
                await self.join_match.execute(match, player)
                break
            except MatchAlreadyReadyException:
                pass  # retry
        return player, match, match_client
