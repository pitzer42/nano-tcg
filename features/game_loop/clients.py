class BaseMatchClient:

    async def wait_update(self):
        raise NotImplementedError()

    async def update(self):
        raise NotImplementedError()
