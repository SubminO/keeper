#!/usr/bin/env python

import argparse
import asyncio
import websockets
import json
from json.decoder import JSONDecodeError

from keeper import Keeper, error
from keeper.frame import Frame
from keeper.geodetector import get_geodetector
from keeper.publisher import Publisher


async def start_keeper(params, _loop=None):
    try:
        geodetector = get_geodetector(params)
        frame_engine = Frame(geodetector)

        publisher = Publisher(params, _loop)
        await publisher.connect()

        keeper = Keeper(frame_engine, publisher)

        uri = f"ws://{params.wsaddr}{params.wspath}:{params.wsport}"
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                try:
                    await keeper.serve(json.loads(message))
                except JSONDecodeError:
                    # todo logging
                    pass
                except error.KeeperError as e:
                    print(e)
                    break

        await publisher.destroy()
    except error.KeeperBackendConnectionError as e:
        # todo организовать обработку прочик исключений
        pass
    except error.KeeperError:
        pass


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()

    # WEBSOCKET CONNECTION
    args_parser.add_argument('--wsaddr', default='127.0.0.1', help='IP address for websocket ws')
    args_parser.add_argument('--wspath', default='', help='Path to websocket')
    args_parser.add_argument('--wsport', default=8080, help='Port for websocket ws')

    # GEODETECTOR DATABASE (redis or postgresql)
    args_parser.add_argument('--geobackend', default='redis', help='Backend to be used to determine the geodata')
    args_parser.add_argument('--gbhost', default='localhost', help='The geodetector database host')
    args_parser.add_argument('--gbport', required=True, help='The geodetector database port')
    args_parser.add_argument('--gbuser', default=None, help='The geodetector database user')
    args_parser.add_argument('--gbpass', default=None, help='The geodetector database password')
    args_parser.add_argument('--gbdb', default=None, help='The geodetector database name/index. Depended at geobakend')

    # GEODETECTOR PARAMS
    args_parser.add_argument('--location', required=True, help='The location name on which the database is configured')
    args_parser.add_argument('--rradius', required=True, help='Radius around the route point at which registered geo points will be searched')
    args_parser.add_argument('--runit', default='m', help='Unit of the route point radius')
    args_parser.add_argument('--pradius', required=True, help='Radius around the platform point at which registered geo points will be searched')
    args_parser.add_argument('--punit', default='m', help='Unit of the platform point radius')

    # GEODETECTOR DATABASE SOURCE (Postgresql)
    args_parser.add_argument('--gbdshost', default='localhost', help='The geodetector database source of data host')
    args_parser.add_argument('--gbdsport', default=5432, help='The geodetector database source of data port')
    args_parser.add_argument('--gbdsuser', required=True, help='The geodetector database source of data user')
    args_parser.add_argument('--gbdspass', required=True, help='The geodetector database source of data password')
    args_parser.add_argument('--gbdsdb', required=True, help='The geodetector database source of data name/index')

    # QUEUE MESSAGES SERVICE (RabbitMQ)
    args_parser.add_argument('--rmqhost', default='localhost', help='QUeue messages service host')
    args_parser.add_argument('--rmqport', default=5672, help='QUeue messages service port')
    args_parser.add_argument('--rmquser', default='guest', help='QUeue messages service user')
    args_parser.add_argument('--rmqpass', default='guest', help='QUeue messages service password')

    args_parser.add_argument('--debug', action='store_true', help='Debug mode turn on')

    run_params = args_parser.parse_args()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_keeper(run_params, loop))
    except KeyboardInterrupt:
        print("Keyboard interrupt signal accepted. Stopping")
        loop.close()
