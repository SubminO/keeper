from aio_pika import connect, Message
import json


class Publisher:
    def __init__(self, params, loop):
        self.loop = loop
        self.conn = None
        self.channel = None
        self.dsn = f"amqp://{params.rmquser}:{params.rmqpass}@{params.rmqhost}:{params.rmqport}/"

    async def connect(self):
        # Perform connection
        self.conn = await connect(self.dsn, loop=self.loop)

        # Creating a channel
        self.channel = await self.conn.channel()

    async def push(self, violation, critical=False):
        try:
            # Sending the message
            message = json.dumps({
                "violation": violation.name,
                "uid": violation.vehicle.uid,
                "speed": violation.vehicle.speed,
                "route": violation.vehicle.route,
                "datetime": violation.vehicle.datetime,
                "longitude": violation.vehicle.longitude,
                "latitude": violation.vehicle.latitude,
                "critical": critical,
            })

            await self.channel.default_exchange.publish(
                Message(message.encode('utf-8')),
                routing_key=violation.name,
            )
        except (KeyError, AttributeError, TypeError):
            # todo логирование
            pass

    async def destroy(self):
        await self.conn.close()
