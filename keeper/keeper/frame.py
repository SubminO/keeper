from keeper import error


class Frame:
    _base_fields = {"time", "uid", "datetime", "posinfo"}
    # _posinfo_fields = {"longitude", "latitude", "altitude", "speed", "course", "satellites"}
    _posinfo_fields = {"longitude", "latitude", "speed"}

    def __init__(self, geodetector):
        self.gd = geodetector

    def get_frames(self, raw_data):
        if not isinstance(raw_data, (dict, list)):
            raise error.KeeperFrameTypeError

        raw_data = [raw_data] if isinstance(raw_data, dict) else raw_data

        data = [{**bit, **bit.pop("posinfo")} for bit in raw_data if self._is_valid(bit)]
        return ({**bit, "around": self._get_araound(bit)} for bit in data)

    def _is_valid(self, data):
        # все нужные поля должны присутствовать.
        # В идеале, валидация типов тоже нужна.
        try:
            return all([
                self._base_fields.issubset(data.keys()),
                self._posinfo_fields.issubset(data["posinfo"].keys())
            ])
        except KeyError:
            return False

    def _get_araound(self, posinfo) -> dict:
        around = {
            "route": {},
            "platform": {}
        }

        route_points, platform_points = self.gd.georadius(posinfo["longitude"],
                                                          posinfo["latitude"])

        self._fullfill_around(around["route"], route_points)
        self._fullfill_around(around["platform"], platform_points)

        return around

    def _fullfill_around(self, target: dict, points: list) -> None:
        for route, idx in points:
            if route in target:
                target[route].append(idx)
            else:
                target[route] = [idx]
