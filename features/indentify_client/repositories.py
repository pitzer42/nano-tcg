from abc import ABC


class IdentityRepository(ABC):
    async def is_client_id_available(self, client_id) -> bool:
        raise NotImplementedError()

    async def make_client_id_unavailable(self, client_id: str):
        raise NotImplementedError()
