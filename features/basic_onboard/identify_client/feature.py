from features.basic_onboard.identify_client.clients import IdentifiableClient
from features.basic_onboard.identify_client.repositories import IdentityRepository


class IdentifyClient:

    def __init__(self,
                 client: IdentifiableClient,
                 repo: IdentityRepository):
        self.client = client
        self.repo = repo

    async def execute(self):
        while True:
            client_id = await self.client.request_client_id()
            client_id_available = await self.repo.is_client_id_available(client_id)
            if client_id_available:
                await self.repo.make_client_id_unavailable(client_id)
                return client_id
