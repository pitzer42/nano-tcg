from entities.match import Match
from features.basic_onboard.select_or_create_match.clients import SelectOrCreateMatchClient
from features.basic_onboard.select_or_create_match.repositories import SelectOrCreateMatchRepository, \
    CreateMatchException


class SelectOrCreateMatch:

    def __init__(self,
                 client: SelectOrCreateMatchClient,
                 matches: SelectOrCreateMatchRepository,
                 match_factory,
                 match_client_factory):
        self.client = client
        self.matches = matches
        self.match_factory = match_factory
        self.match_client_factory = match_client_factory

    async def execute(self):
        while True:
            waiting_matches = await self.matches.get_waiting_matches()
            match_id, password = await self.client.request_match_id_and_password(waiting_matches)

            try:
                match = await self.select(match_id, password)
            except AttributeError:
                # there is no match with id == match_id
                match = await self.create(match_id, password)
            except WrongMatchPasswordException:
                # wrong password was provided, retry
                continue

            match_client = await self.match_client_factory(match_id)
            return match, match_client

    async def select(self, match_id, password: str) -> Match:
        match: Match = await self.matches.get_by_id(match_id)
        if match.check_password(password):
            return match
        else:
            await self.client.alert_wrong_match_password(match)
            raise WrongMatchPasswordException()

    async def create(self, match_id, password):
        try:
            match = self.match_factory(
                match_id,
                password
            )
            await self.matches.save_match(match)
            return match
        except CreateMatchException as exception:
            await self.client.alert_match_creation_exception(exception)


class WrongMatchPasswordException(Exception):
    pass
