from keeper.settings import *
from keeper.vehicles import Vehicle


class Violation:
    def __init__(self, handler, name: str, vehicle: Vehicle, max_value: int):
        self._handler = handler
        self._max_value = max_value

        self.name = name
        self.vehicle = vehicle
        self.value = 0

    async def inc(self) -> None:
        self.value += 1

        if self.value >= self._max_value:
            await self._handler(self, True)
        else:
            await self._handler(self, False)

    async def dec(self) -> None:
        if self.value > 0:
            self.value = 0 if VIOLATION_STRATEGY == "FAST" else (self.value - 1)
