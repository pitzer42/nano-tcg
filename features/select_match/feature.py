from repositories.match import MatchRepository


class SelectMatch:

    def __init__(self, match_repo: MatchRepository):
        self.match_repo = match_repo

    async def execute(self, match_id):
        match = self.match_repo.get_match_by_id(match_id)
        await self.match_repo.insert_match(match)
