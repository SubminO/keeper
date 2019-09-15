from keeper.settings import *
from keeper.violation import Violation


class Vehicle:
    __slots__ = ("uid", "speed", "around", "time", "datetime", "longitude", "latitude",
                 "route_violation", "speed_violation", "direction_violation", "route_lost_violation",
                 "_route_detect_retries", "_route", "_prev_irps", "_prev_route_points", "publisher")

    def __init__(self, data, publisher):
        self.uid: str = data['uid']
        self.speed: int = data['speed']
        self.around: dict = data['around']
        self.time: int = data['time']
        self.datetime: str = data['datetime']
        self.longitude: float = data['longitude']
        self.latitude: float = data['latitude']

        self.route_violation = Violation(publisher.push, 'route_violation', self, MAX_ROUTE_VIOLATIONS)
        self.route_lost_violation = Violation(publisher.push, 'route_lost_violation', self, MAX_ROUTE_DETECT_LOSTS)
        self.direction_violation = Violation(publisher.push, 'direction_violation', self, MAX_DIRECTION_VIOLATIONS)
        self.speed_violation = Violation(publisher.push, 'speed_violation', self, MAX_SPEED_VIOLATIONS)

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

    def update(self, data: dict) -> None:
        try:
            for key, value in data.items():
                if not key.startswith("_"):
                    setattr(self, key, value)
        except AttributeError:
            # атрибуты не из слота игнорируем
            pass

    async def detect_route(self):
        # todo предусмотреть отключения автоопределения моршрута и перевода его в ручной режим
        # нельзя давать возможность кататься вне маршрута вне рабочего имени
        if self._route_detect_retries < MAX_ROUTE_DETECT_RETRIES:
            # todo учесть время работы этого ТС на данном маршруте
            self._route_detect_retries += 1
        else:
            # todo что делать если попытки определить маршрут закончились?
            self._route_detect_retries = None

        route = set(self.around['route'].keys())

        if route:
            await self.route_lost_violation.dec()

        if not route:
            # траспорт съехал с маршрута до определения последнего
            await self.route_lost_violation.inc()
        elif len(self._route) > 1:
            self._route = self._route & route
        else:
            self._route = route

    async def check_route(self):
        """проверка следованию установленного маршрута"""
        if self.around['route'].get(self.route):
            await self.route_violation.dec()
        else:
            await self.route_violation.inc()

    async def check_direction(self):
        """проверка следованию прямому направлению движения по маршруту"""
        route_points = set(self.around['route'].get(self.route, []))
        irps = self._prev_route_points & route_points

        try:
            if max(self._prev_irps) < max(irps):
                await self.direction_violation.dec()
            else:
                await self.direction_violation.inc()
        except ValueError:
            pass

        self._prev_route_points = route_points
        self._prev_irps = irps

    async def check_speed(self):
        """проверка соблюдения скоростного режима"""
        if self.speed < MAX_SPEED:
            await self.speed_violation.dec()
        else:
            await self.speed_violation.inc()


class Vehicles:
    def __init__(self, backend):
        self.publisher = backend.publisher
        self.dbsrc = backend.dbsrc

        self._vehicles = dict()

    def produce(self, data):
        """обновляет или регистрирует ТС"""
        try:
            vehicle = self._vehicles[data["uid"]]
            vehicle.update(data)
            return vehicle
        except KeyError:
            self._vehicles[data["uid"]] = Vehicle(data, self.publisher)
            return self._vehicles[data["uid"]]

    async def garbage_collector(self):
        """Собирает данные об ТС, от которых давно не приходили данные """
        # todo garbage_collector()
        pass
