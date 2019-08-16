from .socket import Socket
from .frame import Frame
from .vehicles import Vehicles
from .errors import *


class Keeper:
    def __init__(self, sockpath="/var/run/egtsd.sock"):
        self.client = Socket(sockpath).connect()
        self.vehicles = Vehicles()
        self.frame = Frame()

    def serve(self):
        while True:
            try:
                data = self.client.read()
                if not data:
                    raise KeeperSocketClosedError()

                for frame in [self.frame.init(chunk) for chunk in data]:
                    if self.vehicles[frame]:
                        if not self.vehicles[frame].route_detected:
                            self.vehicles[frame].detect_route()
                    else:
                        self.vehicles.register(frame)

                    # только для ТС с определенным маршрутом можно проверять маршрут и остановки
                    if self.vehicles[frame].route_detected and len(self.vehicles[frame].route) == 1:
                        self.vehicles[frame].check_route(frame)
                        self.vehicles[frame].check_platform(frame)
                        self.vehicles[frame].check_direction(frame)

            except KeeperSocketClosedError as e:
                # todo logging
                break
            except Exception:
                pass
