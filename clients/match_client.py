from abc import ABC


class MatchClient(ABC):
    async def notify_new_player_join(self, player):
        raise NotImplementedError()

    async def notify_match_start(self, match):
        raise NotImplementedError()

    def wait_update(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
