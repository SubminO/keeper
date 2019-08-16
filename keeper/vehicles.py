from .errors import *


class Vehicle:
    def __init__(self, data):
        self._data = data
        self._route = set()

    @property
    def route(self):
        return self._route

    @property
    def route_detected(self):
        return True if len(self._route) == 1 else False

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
        self._data = dict()

    def __getitem__(self, frame):
        if not isinstance(frame, dict):
            raise KeeperFrameError("Invalid frame type")
        if 'vin' not in frame:
            raise KeeperFrameStructureError("Invalid frame type")

        return self._data[frame['vin']]

    def __iter__(self):
        return self._data

    def __len__(self):
        return len(self._data.keys())

    def has_registered(self, data):
        return True if data["vin"] in self._data else False

    def register(self, data):
        self._data[data["vin"]] = Vehicle(data)
