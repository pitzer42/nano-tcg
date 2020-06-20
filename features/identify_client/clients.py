from abc import ABC


class IdentifiableClient(ABC):

    async def request_client_id(self) -> str:
        raise NotImplementedError()
