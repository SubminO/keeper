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
    def uin(self):
        return self._data['uin']

    @property
    def longitude(self):
        return self._data['longitude']

    # @longitude.setter
    # def longitude(self, value):
    #     self._data['longitude'] = value

    @property
    def latitude(self):
        return self._data['latitude']

    # @latitude.setter
    # def latitude(self, value):
    #     self._data['latitude'] = value

    @property
    def speed(self):
        return self._data['speed']

    # @speed.setter
    # def speed(self, value):
    #     self.last_speed = self._data['speed']
    #     self._data['speed'] = value

    @property
    def route(self):
        return self._route

    # @route.setter
    # def route(self, value):
    #     pass

    def detect_route(self):
        # belong = vehicle["route"].isdisjoint(set(frame['around']['route'].keys()))
        #
        # # маршрут не определен, кол-во нарушений не превысило критический порог
        # if belong and vehicle["route_violation"] < app.config.max_route_violations:
        #     vehicle["route_violation"] + +
        # # маршрут не определен, кол-во нарушений превысило критический порог
        # else if belong and vehicle["route_violation"] >= app.config.max_route_violations:
        #     raise VehicleRouteDetectError("Route detection error")
        #
        # vehicle['route'] = vehicle['route'] & frame['around']['route'].keys()
        #
        # if len(vehicle['route']) == 1:
        #     vehicle['route_detected'] = 1

        pass

    def check_route(self):
        pass

    def check_platform(self):
        pass

    def check_direction(self):
        pass

    def update(self, new_data):
        return self


class Vehicles:
    def __init__(self):
        self._vehicles = dict()

    def register(self, data):
        self._vehicles[data["uin"]] = Vehicle(data)
        return self._vehicles[data['uin']]

    def produce(self, data):
        if data['uin'] in self._vehicles:
            return self._vehicles[data['uin']].update(data)
        else:
            return self.register(data)
