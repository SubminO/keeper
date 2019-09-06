from keeper import error


class Frame:
    _base_fields = {"time", "uid", "datetime", "posinfo"}
    _posinfo_fields = {"longitude", "latitude", "altitude", "speed", "course", "satellites"}

    def __init__(self, geodetector):
        self.gd = geodetector

    def get_frames(self, raw_data):
        if not isinstance(raw_data, (dict, list, tuple)):
            raise error.KeeperFrameTypeError

        raw_data = raw_data if isinstance(raw_data, dict) else [raw_data]

        data = [{**bit, **bit.pop("posinfo")} for bit in raw_data if self._is_valid(bit)]
        return ({**bit, bit["around"]: self.get_araound(bit)} for bit in data)

    def _is_valid(self, data):
        # все нужные поля должны присутствовать.
        # В идеале, валидация типов тоже нужна.
        content_is_valid = all([
            self._base_fields.issubset(data.keys()),
            self._posinfo_fields.issubset(data["posinfo"].keys())
        ])

        if not content_is_valid:
            # todo logging on error.KeeperFrameStructureError
            pass

        return content_is_valid

    def get_araound(self, posinfo):
        # around = dict()

        points = self.gd.georadius(posinfo["longitude"], posinfo["latitude"])
        return points

        # for point in [point.split('_') for point in points]:
        #     if point[0] not in around:
        #         around[point[0]] = dict()
        #     if point[1] not in around[point[0]]:
        #         around[point[0]][point[1]] = list()
        #
        #     around[point[0]][point[1]].append(int(point[2]))
