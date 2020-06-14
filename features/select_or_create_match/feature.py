from features.create_match.feature import CreateMatch
from features.select_match.feature import SelectMatch
from .clients import SelectOrCreateMatchClient


class SelectOrCreateMatch:

    def __init__(self,
                 client: SelectOrCreateMatchClient,
                 select_match: SelectMatch,
                 create_match: CreateMatch):
        self.client = client
        self.create_match = create_match
        self.select_match = select_match

    async def execute(self):
        option = await self.client.request_select_or_create_match()
        if option:
            return await self.select_match.execute()
        return await self.create_match.execute()
