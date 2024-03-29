from keeper.settings import *
from keeper.violation import Violation
from keeper.geodetector import get_distance


class Vehicle:
    __slots__ = ("uid", "speed", "around", "time", "datetime", "longitude", "latitude", "_prev_time",
                 "route_violation", "speed_violation", "direction_violation", "route_lost_violation",
                 "_route_detect_retries", "_route", "_prev_irps", "_prev_route_points", "publisher",
                 "_prev_longitude", "_prev_latitude", "geo_speed")

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

        self._prev_time = 0
        self._prev_longitude = 0.0
        self._prev_latitude = 0.0
        self.geo_speed = 0.0

    @property
    def route_detected(self):
        return True if len(self._route) == 1 else False

    @property
    def route(self):
        routes = list(self._route)
        return routes[0] if self.route_detected else routes

    @property
    def restricted(self):
        return True if self.time - self._prev_time > RESTRICTED_TIME else False

    def update(self, data: dict) -> None:
        for key, value in data.items():
            try:
                setattr(self, f"_prev_{key}", getattr(self, key))
                setattr(self, key, value)
            except AttributeError:
                # атрибуты не из слота игнорируем
                pass

        self._set_geo_speed()

    async def detect_route(self):
        # todo предусмотреть отключения автоопределения моршрута и перевода его в ручной режим
        # нельзя давать возможность кататься вне маршрута вне рабочего имени
        if self._route_detect_retries < MAX_ROUTE_DETECT_RETRIES:
            # todo учесть время работы этого ТС на данном маршруте
            self._route_detect_retries += 1
        else:
            # todo что делать если попытки определить маршрут закончились?
            self._route_detect_retries = 0

        route = set(self.around['route'].keys())

        if route:
            await self.route_lost_violation.dec()
        else:
            # траспорт съехал с маршрута до определения последнего
            await self.route_lost_violation.inc()

        # подумать здесь
        if len(self._route) > 1:
            self._route = self._route & route

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
        if float(self.speed) >= MAX_SPEED:
            await self.speed_violation.inc()
        elif self.geo_speed >= MAX_SPEED:
            await self.speed_violation.inc()
        else:
            await self.speed_violation.dec()

    def _set_geo_speed(self):
        distance = get_distance(
            (self._prev_latitude, self._prev_longitude),
            (self.latitude, self.longitude)
        )

        # Speed of vehicle calculated by geospatials and time diff (km/h)
        self.geo_speed = 3600 * distance / (self.time - self._prev_time)


class Vehicles:
    def __init__(self, backend):
        self.publisher = backend.publisher

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
