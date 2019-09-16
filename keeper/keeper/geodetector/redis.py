import redis
from keeper import error


class Detector:
    def __init__(self, params, gdbs):
        """Геодетектор с бекэндом в redis"""
        self.location = params.location
        self.rradius = params.rradius
        self.pradius = params.pradius
        self.runit = params.runit
        self.punit = params.punit

        self.host: str = params.gbhost
        self.port: int = params.gbport
        self.password: str = params.gbpass
        self.db = params.gbdb

        # Geodetector data backend source
        self._gdbs = gdbs

        # Geodetector bgandler
        self._dbh = None

    def connect(self):
        try:
            self._dbh = redis.Redis(host=self.host,
                                    port=self.port,
                                    db=self.db,
                                    password=self.password)

        except Exception as e:
            raise error.KeeperBackendConnectionError(e)

    def load_geodata(self) -> None:
        self._gdbs.cursor.execute(
            "SELECT r.name, rp.order_number, rp.longitude, rp.latitude FROM route_point rp"
            " INNER JOIN route r ON (rp.route_id = r.id)"
            " WHERE rp.longitude IS NOT NULL AND rp.latitude IS NOT NULL"
            "   AND rp.order_number IS NOT NULL AND rp.route_id IS NOT NULL "
        )
        self._geoadd(f"{self.location}_route", self._gdbs.cursor.fetchall())

        self._gdbs.cursor.execute(
            "SELECT r.name, rp.order_number, rp.longitude, rp.latitude FROM route_point rp"
            " INNER JOIN route r ON (rp.route_id = r.id)"
            " WHERE rp.longitude IS NOT NULL AND rp.latitude IS NOT NULL AND rp.order_number IS NOT NULL"
            "   AND  rp.route_id IS NOT NULL AND rp.route_platform_id IS NOT NULL"
        )
        self._geoadd(f"{self.location}_platform", self._gdbs.cursor.fetchall())

    def reload_geodata(self, force=False):
        if force:
            # self._dbh.zrem(self.location)
            self.load_geodata()

    def georadius(self, longitude, latitude):
        geospatial = [longitude, latitude]

        route_points = [tuple(p.decode().split("_")) for p in self._dbh.georadius(f"{self.location}_route",
                                                                                  *geospatial,
                                                                                  self.rradius,
                                                                                  self.runit)]

        platform_points = [tuple(p.decode().split("_")) for p in self._dbh.georadius(f"{self.location}_platform",
                                                                                     *geospatial,
                                                                                     self.pradius,
                                                                                     self.punit)]

        return route_points, platform_points

    def _geoadd(self, name, items):
        geospatials = []
        for route, number, lon, lat in items:
            geospatials.extend([lon, lat, f"{route}_{number}"])

        self._dbh.geoadd(name, *geospatials)
