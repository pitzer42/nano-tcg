from abc import ABC


class PlayerRepository(ABC):

    async def make_player_id_unavailable_if_is_available(self, player_id) -> bool:
        raise NotImplementedError()
