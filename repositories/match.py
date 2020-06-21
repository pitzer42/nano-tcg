from abc import ABC


class MatchRepository(ABC):

    async def get_match_by_id(self, match_id):
        raise NotImplementedError()

    async def insert_match(self, match):
        raise NotImplementedError()

    async def get_waiting_matches(self):
        raise NotImplementedError()

    async def join_if_still_waiting(self, player, match):
        raise NotImplementedError()
