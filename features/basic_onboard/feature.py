from entities.player import Player
from features.basic_onboard.identify_client.feature import IdentifyClient
from features.basic_onboard.join_match.feature import JoinMatch
from features.basic_onboard.join_match.repositories import MatchAlreadyReadyException
from features.basic_onboard.select_or_create_match.feature import SelectOrCreateMatch


class BasicOnboard:

    def __init__(self,
                 identify_client: IdentifyClient,
                 select_or_create_match: SelectOrCreateMatch,
                 join_match: JoinMatch):
        self.identify_client = identify_client
        self.select_or_create_match = select_or_create_match
        self.join_match = join_match

    async def execute(self):
        client_id = await self.identify_client.execute()
        player = Player(client_id)
        while True:
            match, match_client = await self.select_or_create_match.execute()
            self.join_match.match_client = match_client
            try:
                await self.join_match.execute(match, player)
                break
            except MatchAlreadyReadyException:
                pass  # retry
        return player, match, match_client
