from entities.match import Match


class JoinMatchRepository:

    async def join_and_get_if_still_waiting(self, match: Match, player):
        raise NotImplementedError()


class MatchAlreadyReadyException(Exception):
    pass
