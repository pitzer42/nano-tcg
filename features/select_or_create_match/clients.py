from abc import ABC


class SelectOrCreateMatchClient(ABC):
    async def request_select_or_create_match(self) -> bool:
        raise NotImplementedError()
