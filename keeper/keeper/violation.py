from keeper.settings import *


class Violation:
    def __init__(self, handler, name: str, vehicle, max_value: int):
        self._handler = handler
        self._max_value = max_value

        self.name = name
        self.vehicle = vehicle
        self.value = 0

    async def inc(self) -> None:
        if not self.vehicle.restricted:
            return

        # Sending the message
        message = {
            "violation": self.name,
            "uid": self.vehicle.uid,
            "board_speed": self.vehicle.speed,
            "geo_speed": self.vehicle.geo_speed,
            "route": self.vehicle.route,
            "datetime": self.vehicle.datetime,
            "longitude": self.vehicle.longitude,
            "latitude": self.vehicle.latitude,
        }

        if self.value < self._max_value:
            self.value += 1

        message["critical"] = True if self.value >= self._max_value else False

        await self._handler(self, "violation", message)

    async def dec(self) -> None:
        if not self.vehicle.restricted:
            return

        if self.value > 0:
            self.value = 0 if VIOLATION_STRATEGY == "FAST" else (self.value - 1)
