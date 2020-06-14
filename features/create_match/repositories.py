from features.create_match.entities import Match


class CreateMatchException(Exception):
    async def create_match(self, match: Match):
        raise NotImplementedError()
