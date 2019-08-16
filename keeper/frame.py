import json
from .errors import *

class Frame:
    _fields = {'vin', 'speed', 'longitude', 'lattitude'}

    def init(self, data):
        try:
            chunks = json.loads(data.decode("utf-8").replace("][", ","))
        except Exception as e:
            raise Exception

        return [chunk for chunk in chunks if self._is_valid(chunk)]

    def _is_valid(self, chunk):
        return self._fields.issubset(chunk.keys())
