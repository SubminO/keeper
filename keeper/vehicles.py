from .errors import *


class Vehicle:
    def __init__(self, data):
        self._data = data
        self._route = set()

        self.last_speed = 0

        self.route_violation = 0
        self.platform_violation = 0
        self.direction_violation = 0

        self.prev_route_point = None
        self.prev_platform_point = None
        self.prev_point = None
        self.prev_platform = None

        self.next_route_point = None
        self.next_platform_point = None
        self.next_point = None
        self.next_platform = None

    @property
    def route_detected(self):
        return True if len(self._route) == 1 else False

    @property
    def vin(self):
        return self._data['vin']

    @property
    def longitude(self):
        return self._data['longitude']

    @longitude.setter
    def longitude(self, value):
        self._data['longitude'] = value

    @property
    def latitude(self):
        return self._data['latitude']

    @latitude.setter
    def latitude(self, value):
        self._data['latitude'] = value

    @property
    def speed(self):
        return self._data['speed']

    @speed.setter
    def speed(self, value):
        self._data['speed'] = value

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, value):
        pass

    def detect_route(self):
        pass

    def check_route(self):
        pass

    def check_platform(self):
        pass

    def check_direction(self):
        pass


class Vehicles:
    def __init__(self):
        self._vehicles = dict()

    def register(self, data):
        self._vehicles[data["vin"]] = Vehicle(data)
        return self._vehicles[data['vin']]

    def produce(self, data):
        if data['vin'] in self._vehicles:
            return self._vehicles[data['vin']]
        else:
            return self.register(data)
