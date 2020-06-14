from abc import ABC


class CreateMatchClient(ABC):
    async def request_new_match_id(self) -> str:
        raise NotImplementedError()

    async def request_new_match_password(self) -> str:
        raise NotImplementedError()

    async def alert_match_creation_exception(self, exception):
        raise NotImplementedError()
