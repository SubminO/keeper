from keeper.settings import *
from keeper.violation import Violation


class Vehicle:
    __slots__ = ("uid", "speed", "around", "route_violation", "_route_detect_retries","speed_violation",
                 "direction_violation", "route_lost_violation", "_route", "_prev_irps", "_prev_route_points")

    def __init__(self, data):
        self.uid: str = data['uid']
        self.speed: int = data['speed']
        self.around: dict = data['around']

        self.route_violation = Violation(None, 'route_violation', data['uid'], MAX_ROUTE_VIOLATIONS)
        self.route_lost_violation = Violation(None, 'route_lost_violation', data['uid'], MAX_ROUTE_DETECT_LOSTS)
        self.direction_violation = Violation(None, 'direction_violation', data['uid'], MAX_DIRECTION_VIOLATIONS)
        self.speed_violation = Violation(None, 'speed_violation', data['uid'], MAX_SPEED_VIOLATIONS)

        # IRPs - intersected_route_points
        self._prev_irps = set()
        self._prev_route_points = set()
        self._route = set()
        self._route_detect_retries = 0

    @property
    def route_detected(self):
        return True if len(self._route) == 1 else False

    @property
    def route(self):
        return list(self._route)[0]

    @route.setter
    def route(self, value: list) -> None:
        # todo предусмотреть отключения автоопределения моршрута и перевода его в ручной режим
        # нельзя давать возможность кататься вне маршрута вне рабочего имени
        if self._route_detect_retries < MAX_ROUTE_DETECT_RETRIES:
            # todo учесть время работы этого ТС на данном маршруте
            self._route_detect_retries += 1
        else:
            self._route_detect_retries = None

        if not value:
            # траспорт съехал с маршрута до определения последнего
            self.route_lost_violation.inc()
        elif len(self._route) > 1:
            self._route = self._route & set(value)
        else:
            self._route = set(value)

        if value:
            self.route_lost_violation.dec()

    def update(self, data: dict) -> None:
        try:
            for key, value in data.items():
                if not key.startswith("_"):
                    setattr(self, key, value)
        except AttributeError:
            # атрибуты не из слота игнорируем
            pass

    def detect_route(self):
        self.route = self.around['route'].keys()

    def check_route(self):
        """проверка следованию установленного маршрута"""
        if self.around['route'].get(self.route):
            self.route_violation.dec()
        else:
            self.route_violation.inc()

    def check_direction(self):
        """проверка следованию прямому направлению движения по маршруту"""
        route_points = set(self.around['route'].get(self.route, []))
        irps = self._prev_route_points & route_points

        try:
            if max(self._prev_irps) < max(irps):
                self.direction_violation.dec()
            else:
                self.direction_violation.inc()
        except ValueError:
            pass

        self._prev_route_points = route_points
        self._prev_irps = irps

    def check_speed(self):
        """проверка соблюдения скоростного режима"""
        if self.speed < MAX_SPEED:
            self.speed_violation.dec()
        else:
            self.speed_violation.inc()


class Vehicles:
    def __init__(self):
        self._vehicles = dict()

    def produce(self, data):
        """обновляет или регистрирует ТС"""
        try:
            vehicle = self._vehicles[data["uid"]]
            vehicle.update(data)
            return vehicle
        except KeyError:
            self._vehicles[data["uid"]] = Vehicle(data)
            return self._vehicles[data["uid"]]

    def garbage_collector(self):
        """Собирает данные об ТС, от которых давно не приходили данные """
        # todo garbage_collector()
        pass
