from clients.player_client import PlayerClient
from repositories.match import MatchRepository
from repositories.player import PlayerRepository


class Onboard:

    def __init__(self,
                 client: PlayerClient,
                 create_player,
                 player_repo: PlayerRepository,
                 match_factory,
                 match_repo: MatchRepository,
                 create_match_client):
        self.client = client
        self.create_player = create_player
        self.player_repo = player_repo
        self.match_factory = match_factory
        self.match_repo = match_repo
        self.create_match_client = create_match_client

    async def execute(self):
        player = await self.login()
        match, match_client = await self.join_match(player)
        return player, match, match_client

    async def login(self):
        while True:
            player_id = await self.client.request_player_id()
            player_id_was_available = await self.player_repo.make_player_id_unavailable_if_is_available(player_id)
            if player_id_was_available:
                return self.create_player(player_id)
            await self.client.notify_unavailable_player_id(player_id)

    async def join_match(self, player):
        while True:
            match, match_client = await self.select_or_create_match()
            joined = await self.match_repo.join_if_still_waiting(player, match)
            if joined:
                await match_client.notify_new_player_join(player)
                if match.is_ready():
                    match.yield_priority()  # start match
                    await match_client.notify_match_start(match)
                return match, match_client
            else:
                await self.client.notify_match_has_already_started(match)

    async def select_or_create_match(self):
        while True:
            waiting_matches = await self.match_repo.get_waiting_matches()
            match_id, password = await self.client.request_match_id_and_password(waiting_matches)
            match = await self.match_repo.get_match_by_id(match_id)
            if match:
                if not match.check_password(password):
                    self.client.notify_wrong_password(match)
                    continue  # retry
            else:
                match = self.match_factory(match_id, password)
                await self.match_repo.insert_match(match)
            match_client = await self.create_match_client(match)
            return match, match_client
