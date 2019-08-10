from .socket import Socket
from .frame import Frame
from .vehicles import Vehicles, Vehicle


class Keeper:
    def __init__(self, sockpath="/var/run/egtsd.sock"):
        self.vehicles = Vehicles() # singleton
        self.client = Socket(sockpath).connect()

    def serve(self):
        while True:
            try:
                chunk = self.client.read()
                frame = Frame(chunk).init()
            except AssertionError as e:
                # todo logging
                break



            print(e)

                    try:
                        vin = str(frame["vin"])

                        if vin in vehicles:
                            if !vehicles[vin]["route_detected"]:
                                detect_route(vehicles[vin], frame)
                        else:
                            vehicles[sys.intern(vin)] = init_vehicle(frame)

                        # только для ТС с определенным маршрутом можно проверять маршрут и остановки
                        if vehicles[vin]['route_detected'] and len(vehicles[vin]['route']) == 1:
                            check_route(vehicles[vin], frame)
                            check_platform(vehicles[vin], frame)

                            check_direction(vehicles[vin], frame)
                    except:
                        < EXCEPTION_CODE >

                else:
                    break

