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

        if self.value < self._max_value:
            self.value += 1

        if self.value >= self._max_value:
            await self._handler(self, "violation", True)
        else:
            await self._handler(self, "violation", False)

    async def dec(self) -> None:
        if not self.vehicle.restricted:
            return

        if self.value > 0:
            self.value = 0 if VIOLATION_STRATEGY == "FAST" else (self.value - 1)
