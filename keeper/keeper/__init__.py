from keeper.frame import Frame
from keeper.vehicles import Vehicles
from keeper import error


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

                if vehicle.route_detected:
                    # только для ТС с определенным маршрутом
                    # можно проверять маршрут и остановки
                    vehicle.check_speed()
                    vehicle.check_route()
                    vehicle.check_direction()
                else:
                    # иначе пытаемся определить маршрут
                    vehicle.detect_route()

            self.vehicles.garbage_collector()

        except error.KeeperFrameTypeError:
            pass
        except error.KeeperError:
            pass
