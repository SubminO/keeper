from .publisher import Publisher
from .postgresql import Postgresql


class Backend:
    def __init__(self, params):
        self.dbsrc = Postgresql(params)
        self.publisher = Publisher(params)

    async def connect(self):
        self.dbsrc.connect()
        await self.publisher.connect()

    async def destroy(self):
        self.dbsrc.desctroy()
        await self.publisher.destroy()