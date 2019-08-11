import json


class Frame:
    _fields = {'vin', 'speed', 'longitude', 'lattitude'}

    def __init__(self, string):
        data = json.loads(string.decode("utf-8").replace("][", ","))
        self._data = {vd['vin']: vd for vd in data if self._is_valid(vd)}

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return self._data
        # for key in self._data.keys():
        #     yield key

    def __len__(self):
        return len(self._data.keys())

    def _is_valid(self, vd):
        return self._fields.issubset(vd.keys())
