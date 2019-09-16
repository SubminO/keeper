from .publisher import Publisher
from .postgresql import Postgresql


class Backend:
    def __init__(self, params, loop):
        self.dbsrc = Postgresql(params)
        self.publisher = Publisher(params, loop)

    async def connect(self):
        self.dbsrc.connect()
        await self.publisher.connect()

    async def destroy(self):
        self.dbsrc.desctroy()
        await self.publisher.destroy()