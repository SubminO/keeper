from aio_pika import connect, Message
import json


class Publisher:
    def __init__(self, params, loop):
        self.host = params.rmqhost
        self.port = params.rmqport
        self.user = params.rmquser
        self.password = params.rmqpass

        self._loop = loop
        self._conn = None
        self._channel = None

    async def connect(self):
        dsn = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"

        # Perform connection
        self._conn = await connect(dsn, loop=self._loop)

        # Creating a channel
        self._channel = await self._conn.channel()

    async def destroy(self):
        await self._conn.close()

    async def push(self, routing_key, data):
        try:
            await self._channel.default_exchange.publish(
                Message(json.dumps(data).encode('utf-8')),
                routing_key=routing_key,
            )
        except (KeyError, AttributeError, TypeError):
            # todo логирование
            pass
