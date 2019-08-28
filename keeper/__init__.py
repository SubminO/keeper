import json
from .frame import Frame
from .vehicles import Vehicles
import keeper.errors as error


class Keeper:
    def __init__(self, frame_engine):
        self.vehicles = Vehicles()
        self.frame = frame_engine

    def serve(self, data):
        try:
            for f in self.frame.get_frames(data):
                # Регистрируем транспорт если он не зарегистрирован.
                # Возвращаем ссылку на зарегистрированный транспорт
                vehicle = self.vehicles.produce(f)

                # только для ТС с определенным маршрутом можно проверять маршрут и остановки
                if vehicle.route_detected:
                    vehicle.check_route()
                    vehicle.check_platform()
                    vehicle.check_direction()
                else:
                    # иначе пытаемся определить маршрут
                    vehicle.detect_route()

        except error.KeeperFrameTypeError:
            pass
        except error.KeeperError:
            pass
