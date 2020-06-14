from features.select_match.clients import SelectMatchClient
from features.select_match.repositories import WaitingMatchRepository


class SelectMatch:

    def __init__(self,
                 client: SelectMatchClient,
                 repo: WaitingMatchRepository):
        self.client = client
        self.repo = repo

    async def execute(self):
        while True:
            waiting_matches = await self.repo.get_waiting_matches()
            selected_match = await self.client.choose_one(waiting_matches)
            password = await self.client.request_match_password(selected_match)
            if selected_match.check_password(password):
                return selected_match
            await self.client.alert_wrong_match_password(selected_match)
