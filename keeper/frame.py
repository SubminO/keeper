import json


class Frame:
    _fields = {'vin', 'speed', 'longitude', 'lattitude'}

    def __init__(self, data):
        self._data = json.dumps(data.decode("utf-8").replace("][", ","))

    def init(self):
        return {vd['vin']: vd for vd in self._data if self._is_valid(vd)}

    def _is_valid(self, vd):
        return self._fields.issubset(vd.keys())
