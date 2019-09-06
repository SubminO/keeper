from keeper.settings import *


class Violation:
    def __init__(self, handler, name: str, uid: str, max_value: int):
        self.handler = handler
        self.name = name
        self.uid = uid
        self.max_value = max_value
        self.value = 0

    def inc(self):
        self.value += 1

        if self.value >= self.max_value:
            self.handler(self, True)
        else:
            self.handler(self, False)

    def dec(self):
        if self.value > 0:
            self.value = 0 if VIOLATION_STRATEGY == "FAST" else (self.value - 1)
