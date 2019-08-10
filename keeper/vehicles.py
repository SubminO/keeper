

class Vehicle:
    pass


class Vehicles(dict):
    def __init__(self):
        super().__init__()

        self._vehicles = None

    def add(self, frame):
        pass

    @property
    def vin(self):
        pass

    @property
    def vehicles(self):
        return self._vehicles