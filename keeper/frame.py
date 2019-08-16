from .errors import *


class Frame:
    _fields = {'vin', 'speed', 'longitude', 'latitude'}

    def __init__(self, raw):
        if not isinstance(raw, (dict, list, tuple)):
            raise KeeperFrameTypeError()

        if isinstance(raw, dict):
            raw = [raw]

        self._data = (bit for bit in raw if self._is_valid(bit))

    def __iter__(self):
        return iter(self._data)

    def _is_valid(self, bit):
        return self._fields.issubset(bit.keys())
