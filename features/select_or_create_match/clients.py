from abc import ABC
from typing import Tuple

from entities.match import Match


class SelectOrCreateMatchClient(ABC):

    async def request_match_id_and_password(self, waiting_matches) -> Tuple[str, str]:
        raise NotImplementedError()

    async def alert_wrong_match_password(self, match: Match):
        raise NotImplementedError()

    async def alert_match_creation_exception(self, exception):
        pass
