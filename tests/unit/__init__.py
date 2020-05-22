class AsyncGeneratorMock:
    """
    https://stackoverflow.com/questions/36695256/python-asyncio-how-to-mock-aiter-method
    """

    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
