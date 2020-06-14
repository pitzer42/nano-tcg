from features.create_match.clients import CreateMatchClient
from features.create_match.entities import Match
from features.create_match.repositories import CreateMatchException


class CreateMatch:

    def __init__(self,
                 client: CreateMatchClient,
                 repo: CreateMatchException,
                 match_factory):
        self.client = client
        self.repo = repo
        self.match_factory = match_factory

    async def execute(self) -> Match:
        while True:
            match_id = await self.client.request_new_match_id()
            password = await self.client.request_new_match_password()
            try:
                match = await self.match_factory(
                    match_id,
                    password
                )
                await self.repo.create_match(match)
                return match
            except CreateMatchException as exception:
                await self.client.alert_match_creation_exception(exception)
