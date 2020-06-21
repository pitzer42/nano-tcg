from repositories.match import MatchRepository


class CreateMatch:

    def __init__(self, match_factory, match_repo: MatchRepository):
        self.match_factory = match_factory
        self.match_repo = match_repo

    async def execute(self, match_id, password):
        match = self.match_factory(match_id, password)
        await self.match_repo.insert_match(match)
