import json
from .frame import Frame
from .vehicles import Vehicles
from .errors import *


class Keeper:
    def __init__(self):
        self.vehicles = Vehicles()

    def serve(self, message):
        try:
            # получили вместо JSO>N строки  байты, декодируем
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            for f in Frame(json.loads(message)):
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

        except KeeperError:
            pass
