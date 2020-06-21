class IdentifiableClient:

    async def request_client_id(self) -> str:
        raise NotImplementedError()
